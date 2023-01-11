import pandas as pd
import wandb
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
from math import ceil
from collections import defaultdict
api = wandb.Api(timeout=19)
mpl.rcParams["axes.unicode_minus"] = False


def export_run_name():
    project = "hlsong/drone_flock"
    # runs = api.runs(project , {"$and": [{"config.algorithm_name": 'mat'},]})
    runs = api.runs(project, {"$and": [{"config.algorithm_name": 'mat'}, ]}, order="-created_at")
    run_list = []
    config_list = []
    name_list = []
    state_list = []
    for run in runs:
        config = {k: v for k, v in run.config.items() if not k.startswith('_')}
        config_list.append(config)
        run_list.append('/'.join(run.path))
        name_list.append(run.name)
        state_list.append(run.state)

    config_df = pd.DataFrame.from_records(config_list)
    name_df = pd.DataFrame({'name': name_list})
    run_df = pd.DataFrame({'run': run_list})
    state_df = pd.DataFrame({'state': state_list})
    all_df = pd.concat([name_df, run_df, state_df, config_df, ], axis=1)
    project_config = Path.cwd() / 'data' / f"{project.split('/')[-1]}_configs.csv"
    project_config.parent.mkdir(parents=True, exist_ok=True)
    all_df.to_csv(project_config)


def get_df_from_wandb(env, env_name, scenario, Algo_set, store=True, save_path='./', smooth=1, smooth_method=2, step_lenth=None):
    df_list = []
    # print(f" - scenario:{scenario}")
    # 读取本地数据列表
    file_log_name = 'file_list.txt'
    file_log_path = Path(save_path) / env_name / scenario / file_log_name if Path(save_path).is_absolute() else Path.cwd() / save_path / env_name / scenario / file_log_name
    file_list = {}
    if file_log_path.exists():
        with open(file_log_path, 'r') as f:
            for line in f.readlines():
                wdrun_id = line.strip('\n').split('\t')[0]
                wdrun_name = line.strip('\n').split('\t')[1]
                file_list[wdrun_id] = wdrun_name
    else:
        file_list = {}

    for algo in env[scenario].keys():
        # print(f"  -- algo:{algo}")
        if algo not in Algo_set:
            continue
        curve_list = []
        for run_name in env[scenario][algo]:
            # 判断本地是否有数据文件
            if run_name in file_list.keys():
                data_path = file_list[run_name]
                history = pd.read_csv(data_path)
                history["algorithm"] = algo
                metric_key = "Reward"
            else:
                run = api.run(run_name)
                if run.state != "finished":
                    continue
                config = {k: v for k, v in run.config.items() if not k.startswith("_")}
                # print(f"   --- {run.name}")
                if config["env_name"] == "mujoco":
                    metric_key = (
                        "eval_average_episode_rewards"
                        if algo == "HAPPO"
                        else "faulty_node_-1/eval_average_episode_rewards"
                    )
                elif config["env_name"] == "drone":
                    metric_key = "eval_average_episode_rewards"
                elif config["env_name"] == "football":
                    metric_key = "eval_average_episode_scores"
                else:
                    metric_key = "eval_win_rate"
                # history1 = run.scan_history(keys=["_step", metric_key])
                history = run.history(samples=2000).dropna()[["_step", metric_key]]
                history["algorithm"] = algo
                history["seed"] = config["seed"]
                history["Environment steps"] = history["_step"]
                history["Reward"] = history[metric_key]
                indicator = "Reward"
                # store the data
                if store == True:
                    save_path = Path(save_path) if Path(save_path).is_absolute() else Path.cwd() / save_path
                    env_name = run.config['env_name']
                    if env_name is not None:
                        dir_name = save_path / env_name / scenario / algo
                    Path.mkdir(dir_name, parents=True, exist_ok=True)
                    file_name = dir_name / f"{run.name}.csv"
                    history.to_csv(file_name)
                    with open(file_log_path, 'a') as f:
                        f.write(run_name + '\t' + str(file_name) + '\n')

            # algo name
            if algo == "MAT_jpr":
                history["algorithm"] = "MAJOR"
            elif algo == "MAT_mar":
                history["algorithm"] = "MAR"
            elif algo == "MAPPO_jpr":
                history["algorithm"] = "MAPPO+MAJOR"
            elif algo == "MAPPO_mar":
                history["algorithm"] = "MAPPO+MAR"

            # smooth the data
            if smooth_method == 1 and smooth > 1:
                history["Smooth_Reward"] = history[metric_key].rolling(smooth, min_periods=1).mean()
                indicator = "Smooth_Reward"
            elif smooth_method == 2 and smooth > 1:
                y = np.ones(smooth)
                x = np.asarray(history["Reward"])  # (200, 1)
                x = np.squeeze(x)  # (200,)
                z = np.ones(len(x))
                smoothed_x = np.convolve(x, y, 'same') / np.convolve(z, y, 'same')
                history["Smooth_Reward"] = smoothed_x
                indicator = "Smooth_Reward"
            else:
                indicator = "Reward"
            curve_list.append(history)
        data = pd.concat(curve_list)
        data.reset_index(drop=True, inplace=True)
        df_list.append(data)
    df = pd.concat(df_list)
    df.reset_index(drop=True, inplace=True)
    if step_lenth is not None:
        df = df[df["_step"] < step_lenth]
    return df, indicator


def get_df_from_local(env_name, scenario, data_path, smooth=1, smooth_method=2, step_lenth=None,):
    if Path(data_path).is_absolute():
        data_path = Path(data_path)
    else:
        data_path = Path.cwd() / data_path
    logdir = data_path / env_name / scenario
    df_list = []
    # print(f" - scenario:{scenario}")
    for data_dir in logdir.iterdir():
        if data_dir.is_dir():
            algo = data_dir.parts[-1]
            # print(f"  -- algo:{algo}")
            curve_list = []
            for file in data_dir.rglob('*.csv'):
                # print(f"   --- {file}")
                data = pd.read_csv(file)
                # smooth the data
                if smooth_method == 1 and smooth > 1:
                    data["Smooth_Reward"] = data["Reward"].rolling(smooth, min_periods=1).mean()
                    indicator = "Smooth_Reward"
                elif smooth_method == 2 and smooth > 1:
                    y = np.ones(smooth)
                    x = np.asarray(data["Reward"])  # (200, 1)
                    x = np.squeeze(x)  # (200,)
                    z = np.ones(len(x))
                    smoothed_x = np.convolve(x, y, 'same') / np.convolve(z, y, 'same')
                    data["Smooth_Reward"] = smoothed_x
                    indicator = "Smooth_Reward"
                curve_list.append(data)
            data = pd.concat(curve_list)
            data.reset_index(drop=True, inplace=True)
            df_list.append(data)
        df = pd.concat(df_list)
        df.reset_index(drop=True, inplace=True)
        if step_lenth is not None:
            df = df[df["_step"] < step_lenth]
    return df, indicator


def plot_one_scenario(df, indicator, hue_name, env_name, scenario, colors, smooth=1, save=False, save_path='./plot_result'):
    sns.set_theme(
        style="darkgrid",
        font_scale=2,
        rc={"lines.linewidth": 3},
        # font="Tlwg Mono",
        color_codes=True,
    )
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 10))
    ax.set_title(scenario, fontsize=25)
    sns.lineplot(
        data=df, x="Environment steps", y=indicator, hue="algorithm", palette=colors, ax=ax, errorbar='sd'
    )
    ax.set_xlabel("Environment steps", labelpad=10)
    ax.set_ylabel("Reward", labelpad=10)
    # ax.xaxis.set_major_locator(MultipleLocator(250000))
    # plt.xlabel("Environment steps", fontsize=30)
    # plt.ylabel("Reward", fontsize=30)
    ax.legend(fontsize=20, loc='best')
    # plt.legend(fontsize=25)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    if save == True:
        path = Path(save_path) / env_name / scenario if Path(save_path).is_absolute() else Path.cwd() / save_path / env_name / scenario
        path.mkdir(parents=True, exist_ok=True)
        time_now = datetime.now().strftime("%m-%d-%H-%M-%S")
        file_name = path / f"{env_name}-{scenario}-sm{smooth}-{time_now}.pdf"
        plt.savefig(file_name)
    # plt.show()


def plot_multi_scenario(df_list, indicator_list, hue_name, env_name, scenarioes, colors, nsize, smooth=1, save=False, save_path='./plot_result'):
    assert nsize[0] * nsize[1] >= len(scenarioes)
    sns.set_theme(
        style="darkgrid",
        font_scale=3,
        rc={"lines.linewidth": 5},
        # font="Tlwg Mono",
        color_codes=True,
    )
    fig, axis = plt.subplots(nrows=nsize[0], ncols=nsize[1], figsize=(15*nsize[1], 10*nsize[0]*1.1))

    colors1 = [
        sns.color_palette("husl", 9)[0],  # MAPPO_mar
        sns.color_palette("husl", 9)[6],  # MAPPO_jpr
        sns.color_palette("Set2")[6],  # MAPPO
    ]
    colors2 = [
        sns.color_palette("Set2")[1],  # MAT_mar
        sns.color_palette("husl", 9)[7],  # MAT_jpr
        sns.color_palette("Set2")[0],  # MAT
    ]
    colors_dic = {"MAPPO+MAR": colors1[0],
                  "MAPPO+MAJOR": colors1[1],
                  "MAPPO": colors1[2],
                  "MAR": colors2[0],
                  "MAJOR": colors2[1],
                  "MAT": colors2[2]}

    for i, df, indicator in zip(range(len(scenarioes)), df_list, indicator_list):
        scenario = scenarioes[i]

        if len(axis.shape) > 1:
            ax = axis[i // nsize[1], i % nsize[1]]
        else:
            ax = axis[i]
        font = {'family': 'Times New Roman',
                'size': 35,
                }
        ax.set_title(scenario, fontsize=35)
        if "MAPPO" in df["algorithm"].unique():
            hue_order = ["MAPPO", "MAPPO+MAJOR", "MAPPO+MAR"]

        elif "MAT" in df["algorithm"].unique():
            hue_order = ["MAT", "MAJOR", "MAR"]
        colors = [colors_dic[algorithm] for algorithm in hue_order]
        sns.lineplot(
            data=df, x="Environment steps", y=indicator, hue=hue_name, palette=colors, ax=ax, errorbar='sd', hue_order=hue_order
        )
        ax.set_xlabel('')
        ax.set_ylabel('')
        # ax.xticks(fontsize=30)
        # ax.yticks(fontsize=30)

        # ax.xaxis.set_major_locator(MultipleLocator(250000))
        ax.get_legend().set_visible(False)
        # if scenario == "LeaderFollower_PID":
        #     ax.axhline(y=-10, color='black', linestyle='--', linewidth=2)
    # set labels
    if len(axis.shape) > 1:
        for ax in axis[-1, :]:
            ax.set_xlabel('Environment steps', labelpad=10, fontsize=35)
        for ax in axis[:, 0]:
            ax.set_ylabel('Reward', labelpad=10, fontsize=35)
    else:
        for ax in axis:
            ax.set_xlabel('Environment steps', labelpad=10, fontsize=35)
        axis[0].set_ylabel('Reward', labelpad=10, fontsize=35)

    # 主图加label
    line_mat, label_mat = axis[0, 0].get_legend_handles_labels() if len(axis.shape) > 1 else axis[0].get_legend_handles_labels()
    # line_mapppo, label_mapppo = axis[-1, -1].get_legend_handles_labels() if len(axis.shape) > 1 else axis[-1].get_legend_handles_labels()
    # lines = line_mat + line_mapppo
    # labels = label_mat + label_mapppo
    lines = line_mat
    labels = label_mat
    if len(axis.shape) == 1:
        anchor = (0.5, -0.18)
    elif axis.shape[0] == 2:
        anchor = (0.5, -0.02)
    elif axis.shape[0] == 4:
        anchor = (0.5, 0.05)
    else:
        anchor = (0.5, 0)
    # fig.legend(loc='lower center', ncol=6, handles=lines, labels=labels, labelspacing=0.1, fontsize=45, bbox_to_anchor=anchor)

    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20)
    if save == True:
        path = Path(save_path) / env_name if Path(save_path).is_absolute() else Path.cwd() / save_path / env_name
        path.mkdir(parents=True, exist_ok=True)
        time_now = datetime.now().strftime("%m-%d-%H-%M-%S")
        file_name = path / f"{env_name}-sm{smooth}-{time_now}.pdf"
        plt.savefig(file_name, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    store = True
    save_path = './data'
    step_lenth = None
    smooth = 2
    smooth_method = 2
    save_plot = True
    plot_path = './plot_result'

    from runlist.add_enlist import envlist as ENVLISTa
    env_list = ENVLISTa()

    # env_name = "StarCraft2"
    # scenarios = ["1c3s5z", "3s_vs_5z", "5m_vs_6m", "3s5z_vs_3s6z", "10m_vs_11m"]  # mat
    # scenarios = ["1c3s5z", "3s_vs_5z", "8m_vs_9m", "3s5z_vs_3s6z", "10m_vs_11m", "mmm2"]  # mappo
    # env_name = "mujoco"
    # scenarios = ["8x1-Agent Ant", "3x2-Agent HalfCheetah", "3x1-Agent Hopper", "6x1-Agent walker","10x2-Agent swimmer",]
    # scenarios = ["8x1-Agent Ant", "3x2-Agent HalfCheetah", "3x1-Agent Hopper"]  # mappo
    env_name = "drone"
    scenarios = ["Flock_PID", "LeaderFollower_PID", "Flock_RPM"]
    # scenario =
    # env_name = "football"
    env = env_list[env_name]
    # scenarios = [key for key in env.keys()]

    hue_name = 'algorithm'
    FLAG_NUM = 3

    # Algo_set = ['MAPPO', 'MAPPO_mar', 'MAPPO_jpr', 'MAT', 'MAT_mar', 'MAT_jpr']
    # Algo_set = ['MAPPO', 'MAPPO_mar', 'MAPPO_jpr']
    Algo_set = ['MAT', 'MAT_mar', 'MAT_jpr']

    mappo_smooth_dic = defaultdict(lambda: 2)
    mappo_smooth_dic = {'ant_4x2': 6, '8x1-Agent Ant': 4, 'walker_6x1': 4, 'walker_3x2': 4,
                        "3s_vs_5z": 1, "mmm": 1, "3s5z": 2, "1c3s5z": 1, "8m_vs_9m": 1, "5m_vs_6m": 3, "10m_vs_11m": 2, "3s5z_vs_3s6z": 2,
                        "LeaderFollower_PID": 1, "Flock_PID": 1, "LeaderFollower_RPM": 1, "LeaderFollower_PID": 1,
                        "academy_pass_and_shoot_with_keeper": 1, "academy_counterattack_easy": 1, "academy_3_vs_1_with_keeper": 1,
                        }
    mat_smooth_dic = defaultdict(lambda: 2)
    mat_smooth_dic = {"3s_vs_5z": 1, "mmm": 1, "3s5z": 2, "1c3s5z": 1, "8m_vs_9m": 1, "5m_vs_6m": 3, "10m_vs_11m": 2, "3s5z_vs_3s6z": 2,
                      "LeaderFollower_PID": 1, "Flock_PID": 1, "LeaderFollower_RPM": 1, "LeaderFollower_PID": 1,
                      "academy_pass_and_shoot_with_keeper": 1, "academy_counterattack_easy": 1, "academy_3_vs_1_with_keeper": 1,
                      }
    smooth_dic = mappo_smooth_dic if 'MAPPO' in Algo_set[0] else mat_smooth_dic

    if len(Algo_set) == 3:
        colors = [
            sns.color_palette("husl", 9)[0],
            sns.color_palette("husl", 9)[6],
            sns.color_palette("husl", 9)[7],
        ]
    elif len(Algo_set) == 6:
        colors = [
            sns.color_palette("husl", 9)[0],  # SOTA
            sns.color_palette("husl", 9)[1],
            sns.color_palette("husl", 9)[6],  # MAPPO / MAT (baseline)
            sns.color_palette("husl", 9)[7],
            sns.color_palette("husl", 9)[5],
            sns.color_palette("husl", 9)[3],
        ]

    if FLAG_NUM == 1:
        scenario = '5m_vs_6m'
        print(f"env: {env_name}")
        smooth = smooth_dic.get(scenario, 2)
        df, indicator = get_df_from_wandb(env, env_name, scenario, Algo_set, store, save_path, smooth, smooth_method, step_lenth)
        plot_one_scenario(df, indicator, env_name, hue_name, scenario, colors, smooth, save_plot, plot_path)
    if FLAG_NUM == 2:
        for scenario in scenarios:
            print(f"env: {scenario}")
            smooth = smooth_dic.get(scenario, 2)
            df, indicator = get_df_from_wandb(env, env_name, scenario, Algo_set, store, save_path, smooth, smooth_method, step_lenth)
            plot_one_scenario(df, indicator, env_name, hue_name, scenario, colors, smooth, save_plot, plot_path)
    if FLAG_NUM == 3:
        df_list = []
        indicator_list = []
        map_name = []
        Algo_set1 = ['MAPPO', 'MAPPO_mar', 'MAPPO_jpr']
        Algo_set2 = ['MAT', 'MAT_mar', 'MAT_jpr']
        Algo_set = ['MAPPO', 'MAPPO_mar', 'MAPPO_jpr', 'MAT', 'MAT_mar', 'MAT_jpr']
        for scenario in scenarios:
            smooth = mappo_smooth_dic.get(scenario, 2)
            # if scenario == 'Flock_RPM' or scenario == 'LeaderFollower_RPM':
            # if scenario == 'Flock_RPM':
            if scenario == 'LeaderFollower_RPM':
                continue
            if scenario == 'walker_3x2' or scenario == 'half_3x2':
                continue
            print(f"env: {scenario}")
            df, indicator = get_df_from_wandb(env, env_name, scenario, Algo_set1, store, save_path, smooth, smooth_method, step_lenth)
            df_list.append(df)
            indicator_list.append(indicator)
            map_name.append(scenario)

        # for scenario in scenarios:
        #     if scenario == 'walker_3x2' or scenario == 'half_3x2':
        #         continue
        #     smooth = smooth_dic.get(scenario, 2)
        #     print(f"env: {scenario}")
        #     df, indicator = get_df_from_wandb(env, env_name, scenario, Algo_set2, store, save_path, smooth, smooth_method, step_lenth)
        #     df_list.append(df)
        #     indicator_list.append(indicator)
        #     map_name.append(scenario)

        # PLOT SIX ALGORTHM
        # for scenario in scenarios:
        #     if scenario == 'walker_3x2' or scenario == 'half_3x2':
        #         continue
        #     smooth = smooth_dic.get(scenario, 2)
        #     print(f"env: {scenario}")
        #     df, indicator = get_df_from_wandb(env, env_name, scenario, Algo_set, store, save_path, smooth, smooth_method, step_lenth)
        #     df_list.append(df)
        #     indicator_list.append(indicator)
        #     map_name.append(scenario)
        plots_one_row = 3
        nsize = (ceil(len(map_name) / plots_one_row), plots_one_row)
        plot_multi_scenario(df_list, indicator_list, hue_name, env_name, map_name, colors, nsize, smooth, save_plot, plot_path)
