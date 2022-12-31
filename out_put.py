from collections import defaultdict
from pathlib import Path
import pandas as pd
import wandb
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime

from matplotlib.pyplot import MultipleLocator
api = wandb.Api(timeout=19)

# env_name = "SMAC"
# map_names = ["3s5z"]
# map_names = ["3s_vs_5z", "mmm" , "3s5z" ,"1c3s5z","8m_vs_9m","5m_vs_6m","10m_vs_11m","6h_vs_8z","mmm2","3s5z_vs_3s6z","25m","27m_vs_30m"]
# map_names = ["3s_vs_5z", "mmm", "3s5z", "1c3s5z", "8m_vs_9m", "5m_vs_6m", "10m_vs_11m", "3s5z_vs_3s6z",]

env_name = "mujoco"
map_names = ["ant_4x2", "ant_8x1", "half_6x1", "half_3x2","hopper_3x1", "swimmer_10x2", "walker-6x1", "walker_3x2"]
for map_name in map_names:
    project = f"hlsong/{env_name}_{map_name}"
    print(project)
    runs = api.runs(project)
    dic = defaultdict(list)
    order_key = ['mat_mask', 'mat_jpr', 'mat', 'mappo_maska', 'mappo_jpr', 'mappo']
    algo_name = {'mat_mask': "MAT_mar", 'mat_jpr': "MAT_jpr", 'mat': "MAT", 'mappo_maska': "MAPPO_mar", 'mappo_jpr': "MAPPO_jpr", 'mappo': "MAPPO"}

    for run in runs:
        if run.state != "finished":
            continue
        algo = run.config["algorithm_name"]
        dic[algo].append(run.id)
    # save_path = Path(f"./runlist/{env_name}_{map_name}.txt")
    # save_path.parent.mkdir(parents=True, exist_ok=True)
    # with open(f"{str(save_path)}", "w") as fw:
    save_path = Path(f"./runlist/{env_name}.txt")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(f"{str(save_path)}", "a+") as fw:
        print(f"\t\t\"{map_name}\": {{", file=fw)
        for key in order_key:
            print(f"\t\t\t\"{algo_name[key]}\": [", file=fw)
            for run in dic[key]:
                print(f"\t\t\t\t\"{project}/{run}\",", file=fw)
            print(f"\t\t\t],", file=fw)
        print("\t\t},", file=fw)
