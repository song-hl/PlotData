import pandas as pd
import wandb
from pathlib import Path
import hydra
from omegaconf import DictConfig, OmegaConf
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


def get_df_from_wandb(env, scenario, cfg, smooth):
    df_list = []
    env_name = cfg.env_name
    Algo_set = cfg.algo_set
    save_path = cfg.save_path

    # print(f" - scenario:{scenario}")

    # 读取本地数据列表
    file_log_name = 'file_list.txt'
    file_log_path = Path(save_path) / env_name / scenario / file_log_name if Path(save_path).is_absolute() else Path.cwd() / save_path / env_name / scenario / file_log_name
    file_list = {}
    if file_log_path.exists():                                  # 以前下载过数据
        with open(file_log_path, 'r') as f:
            for line in f.readlines():
                wdrun_id = line.strip('\n').split('\t')[0]      # wandb run id
                wdrun_name = line.strip('\n').split('\t')[1]    # wandb run data store path
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
            else:
                run = api.run(run_name)
                if run.state != "finished":
                    continue
                config = {k: v for k, v in run.config.items() if not k.startswith("_")}
                # print(f"   --- {run.name}")

                history = run.history(samples=2000).dropna()[[cfg.data.step, cfg.data.metric_key]]
                history["algorithm"] = algo
                history["seed"] = config["seed"]

                history[cfg.data.local_step] = history[cfg.data.step]
                history[cfg.data.local_metric_key] = history[cfg.data.metric_key]
                indicator = cfg.data.local_metric_key

                # store the data
                if cfg.store == True:
                    save_path = Path(save_path) if Path(save_path).is_absolute() else Path.cwd() / save_path
                    env_name = run.config['env_name']
                    if env_name is not None:
                        dir_name = save_path / env_name / scenario / algo
                    Path.mkdir(dir_name, parents=True, exist_ok=True)
                    file_name = dir_name / f"{run.name}.csv"
                    history.to_csv(file_name)
                    with open(file_log_path, 'a') as f:
                        f.write(run_name + '\t' + str(file_name) + '\n')

            # algo name substitue
            # t = cfg.algo_sub[algo]
            if cfg.use_sub_name and cfg.algo_sub.get(algo,None) is not None:
                history["algorithm"] = cfg.algo_sub[algo]

            # smooth the data
            # if smooth > 1:
            #     history["Smooth_Reward"] = history[metric_key].rolling(smooth, min_periods=1).mean()
            #     indicator = "Smooth_Reward"

            if smooth > 1:
                y = np.ones(smooth)
                x = np.asarray(history[cfg.data.local_metric_key])  # (200, 1)
                x = np.squeeze(x)  # (200,)
                z = np.ones(len(x))
                smoothed_x = np.convolve(x, y, 'same') / np.convolve(z, y, 'same')
                history[cfg.data.smooth_metric_key] = smoothed_x
                indicator = cfg.data.smooth_metric_key
            else:
                indicator = cfg.data.local_metric_key
            curve_list.append(history)

        data = pd.concat(curve_list)
        data.reset_index(drop=True, inplace=True)
        df_list.append(data)

    df = pd.concat(df_list)
    df.reset_index(drop=True, inplace=True)
    if cfg.step_lenth != 0:
        df = df[df[cfg.data.step] < cfg.step_lenth]
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


def plot_multi_scenario(df_list, indicator_list, colors, nsize, cfg):
    env_name = cfg.env_name
    scenarioes = cfg.scenarios
    assert nsize[0] * nsize[1] >= len(scenarioes)
    # 设置图的风格
    sns.set_theme(
        style="darkgrid",
        font_scale=cfg.plot_cfg.font_scale,
        rc={"lines.linewidth": cfg.plot_cfg.linewidth},
        color_codes=True,
    )
    # cfg
    font_size = cfg.plot_cfg.font_size
    
    # 生成图列表
    fig, axis = plt.subplots(nrows=nsize[0], ncols=nsize[1], figsize=(cfg.plot_cfg.figure_size[0]*nsize[1], cfg.plot_cfg.figure_size[1]*nsize[0]*1.1))

    colors_dic = {"MAPPO+MA2CL": sns.color_palette("husl", 9)[0],
                  "MAPPO+MAJOR": sns.color_palette("husl", 9)[6],
                  "MAPPO": sns.color_palette("Set2")[6],
                  "MA2CL": sns.color_palette("Set2")[1],
                  "MAJOR": sns.color_palette("husl", 9)[7],
                  "MAT": sns.color_palette("Set2")[0]}

    # 画子图
    for i, df, indicator in zip(range(len(scenarioes)), df_list, indicator_list):
        scenario = scenarioes[i]

        if len(axis.shape) > 1:
            ax = axis[i // nsize[1], i % nsize[1]]
        else:
            ax = axis[i]
        # title
        ax.set_title(scenario, fontsize=font_size)
        # 画图顺序
        hue_order = cfg.plot_cfg.hue_order[cfg.algo]

        # 颜色
        colors = [colors_dic[algorithm] for algorithm in hue_order]
        
        # 画线
        sns.lineplot(
            data=df, x=cfg.data.local_step, y=indicator, hue=cfg.hue_name, palette=colors, ax=ax, errorbar='sd', hue_order=hue_order
        )
        # 取消子图label
        ax.set_xlabel('')
        ax.set_ylabel('')

        # ax.xaxis.set_major_locator(MultipleLocator(250000))

        ax.get_legend().set_visible(False)  #

        # 子图中的legend
        line, label = ax.get_legend_handles_labels()
        orders = cfg.plot_cfg.legend_order  # legend 顺序
        ax.legend(loc=0, fontsize=45, handles=[line[i] for i in orders], labels=[label[i] for i in orders])

    # set labels
    if len(axis.shape) > 1:
        for ax in axis[-1, :]:
            ax.set_xlabel(cfg.plot_cfg.xlabel, labelpad=10, fontsize=font_size)
        for ax in axis[:, 0]:
            ax.set_ylabel(cfg.plot_cfg.ylabel, labelpad=10, fontsize=font_size)
    else:
        for ax in axis:
            ax.set_xlabel(cfg.plot_cfg.xlabel, labelpad=10, fontsize=font_size)
        axis[0].set_ylabel(cfg.plot_cfg.ylabel, labelpad=10, fontsize=font_size)

    # 主图加label
    lines, labels = axis[0, 0].get_legend_handles_labels() if len(axis.shape) > 1 else axis[0].get_legend_handles_labels()
    main_lines = [lines[i] for i in orders]
    main_labels = [labels[i] for i in orders]
    anchor = cfg.plot_cfg.main_labels_anchor.get(axis.shape, (0.5, 0))

    fig.legend(loc='lower center', ncol=6, handles=main_lines, labels=main_labels, labelspacing=0.1, fontsize=font_size, bbox_to_anchor=anchor, )

    # 保存图片
    if cfg.save_plot == True:
        save_path = cfg.save_path
        path = Path(save_path) / env_name if Path(save_path).is_absolute() else Path.cwd() / save_path / env_name
        path.mkdir(parents=True, exist_ok=True)
        time_now = datetime.now().strftime("%m-%d-%H-%M-%S")
        file_name = path / f"{env_name}-{time_now}.pdf"
        plt.savefig(file_name, bbox_inches='tight')


@hydra.main(
    config_name="config",
    config_path="./conf",
)
def main(cfg: DictConfig):
    OmegaConf.set_struct(cfg, False)
    store = cfg.store
    save_path = cfg.save_path
    step_lenth = cfg.step_lenth
    smooth = cfg.smooth_length
    smooth_method = cfg.smooth_method
    save_plot = cfg.save_plot
    plot_path = cfg.plot_path

    from runlist.add_enlist import envlist as ENVLIST
    env_list = ENVLIST()

    # NOTE 选择需要画图的环境和地图

    env_name = cfg.env_name
    env = env_list[env_name]
    if cfg.plot_all:
        scenarios = [key for key in env.keys()]
    else:
        scenarios = cfg.scenarios
    hue_name = cfg.hue_name
    FLAG_NUM = 3
    figure_type = cfg.figure_type
    Algo_set = cfg.algo_set
    
    smooth_dic = cfg.smooth_dic
    color_config = cfg.color

    colors = [sns.color_palette(color_config.palette, color_config.cls)[i] for i in color_config.index]

    # if FLAG_NUM == 1:
    #     # 只画一个图
    #     scenario = '5m_vs_6m'
    #     print(f"env: {env_name}")
    #     smooth = smooth_dic.get(scenario, 2)
    #     df, indicator = get_df_from_wandb(env, env_name, scenario, Algo_set, store, save_path, smooth, smooth_method, step_lenth)
    #     plot_one_scenario(df, indicator, env_name, hue_name, scenario, colors, smooth, save_plot, plot_path)
    if figure_type == 'MFOP':
        # 画多个单图
        for scenario in scenarios:
            smooth = smooth_dic.get(scenario, 2)
            if scenario in cfg.skip_scenarios:
                continue
            print(f"env: {scenario}")
            df, indicator = get_df_from_wandb(env, scenario, cfg, smooth)
            plot_one_scenario(df, indicator, env_name, hue_name, scenario, colors, smooth, save_plot, plot_path)
    # if figure_type == 'OFMP':
    else:
        # 画一个多图
        df_list = []
        indicator_list = []
        map_name = []
        for scenario in scenarios:
            smooth = smooth_dic.get(scenario, 2)
            if scenario in cfg.skip_scenarios:
                continue
            print(f"env: {scenario}")
            df, indicator = get_df_from_wandb(env, scenario, cfg, smooth)
            df_list.append(df)
            indicator_list.append(indicator)
            map_name.append(scenario)

        plots_one_row = 3
        nsize = (ceil(len(map_name) / plots_one_row), plots_one_row)
        plot_multi_scenario(df_list, indicator_list, colors, nsize, cfg)


if __name__ == "__main__":
    main()
