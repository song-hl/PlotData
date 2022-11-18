from add_enlist import envlist as ENVLISTa
from visualize import (
    get_df_from_local,
    get_df_from_wandb,
    plot_one_scenario,
    plot_multi_scenario,
)
import pandas as pd
import wandb
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib.pyplot import MultipleLocator
api = wandb.Api(timeout=19)
mpl.rcParams["axes.unicode_minus"] = False


if __name__ == "__main__":
    store = True
    save_path = './data/11-18'
    step_lenth = None
    smooth = 3
    smooth_method = 2
    from_wandb = True
    save_plot = True
    plot_path = './plot_result/11-18'
    env_list = ENVLISTa()
    env_name = 'mujoco'
    env = env_list[env_name]
    scenarios = [key for key in env.keys()]
    print(scenarios)
    scenario = scenarios[0]
    print(f"env: {env_name}")
    print(f"scenario: {scenario}")
    if from_wandb:
        df, indicator = get_df_from_wandb(env, scenario, store, save_path, smooth, smooth_method, step_lenth)
    else:
        df, indicator = get_df_from_local(env_name, scenario, save_path, smooth, smooth_method, step_lenth)
    plot_one_scenario(df, indicator, env_name, scenario, save_plot, plot_path)
