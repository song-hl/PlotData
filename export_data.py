import pandas as pd
import wandb
api = wandb.Api()
from pathlib import Path
def main(class_args):
    # Project is specified by <entity/project-name>
    project = "hlsong/compare"
    runs = api.runs(project)
    summary_list = []
    config_list = []
    name_list = []
    for run in runs:
        if run.state == "finished":
            # run.summary are the output key/values like accuracy.
            # We call ._json_dict to omit large files
            summary_list.append(run.summary._json_dict)

            # run.config is the input metrics.
            # We remove special values that start with _.
            config = {k: v for k, v in run.config.items() if not k.startswith('_')}
            config_list.append(config)

            # run.name is the name of the run.
            name_list.append(run.name)
            
            metrics_dataframe = run.history()
            env_name = run.config['env_name']
            map_name = run.config['scenario']
            algo_name = run.config['algorithm_name']
            if env_name is not None and map_name is not None and algo_name is not None:
                if env_name == 'drone':
                    dir_name = Path.cwd() / project / env_name / map_name / algo_name
                elif env_name == 'mujoco':
                    map_name = f"{map_name}-{run.config['agent_conf']}"
                    dir_name = Path.cwd() / project / env_name / map_name / algo_name
                    metrics_dataframe.rename(columns={'faulty_node_-1/eval_average_episode_rewards': 'eval_average_episode_rewards'}, inplace=True)
                    metrics_dataframe = metrics_dataframe.dropna(axis=0, how='any', subset=['eval_average_episode_rewards'])
            if class_args is not None and algo_name == "mask":
                for class_arg in class_args:
                    if class_arg in run.config:
                        dir_name = dir_name / f"{class_arg}-{run.config[class_arg]}"
            # seed = run.name.split('_')[-2][4:]
            # dir_name = dir_name / f"seed-{seed}"
            Path.mkdir(dir_name, parents=True, exist_ok=True)
            file_name = dir_name / f"{run.name}.csv"
            metrics_dataframe.to_csv(file_name)

    summary_df = pd.DataFrame.from_records(summary_list)
    config_df = pd.DataFrame.from_records(config_list)
    name_df = pd.DataFrame({'name': name_list})
    all_df = pd.concat([name_df, config_df, summary_df], axis=1)
    project_config = Path.cwd() / project / 'project_configs.csv'

    all_df.to_csv(project_config)


if __name__ == "__main__":
    # class_arg = ['num_mini_batch', 'forward_method', 'maska_bsz', 'use_W']
    class_arg = None
    main(class_arg)
