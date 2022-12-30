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

env_name = "SMAC"
map_name = "3s5z"
save_path = Path(f"./runlist/{env_name}_{map_name}.txt")
print(save_path)
project = f"hlsong/{env_name}_{map_name}"
print(project)
runs = api.runs(project)
dic = defaultdict(list)
order_key = ['mat_mask', 'mat_jpr', 'mat', 'mappo_maska', 'mappo_jpr', 'mappo']
algo_name = {'mat_mask': "MAT_pma", 'mat_jpr': "MAT_jpr", 'mat': "MAT", 'mappo_maska': "MAPPO_pma", 'mappo_jpr': "MAPPO_jpr", 'mappo': "MAPPO"}

for run in runs:
    if run.state != "finished":
        continue
    algo = run.config["algorithm_name"]
    dic[algo].append(run.id)
save_path = Path(f"./runlist/{env_name}_{map_name}.txt")
save_path.parent.mkdir(parents=True, exist_ok=True)
with open(f"{str(save_path)}", "w") as fw:
    print(f"\t\t\"{map_name}\": {{", file=fw)
    for key in order_key:
        print(f"\t\t\t\"{algo_name[key]}\": [", file=fw)
        for run in dic[key]:
            print(f"\t\t\t\t\"{project}/{run}\",", file=fw)
        print(f"\t\t\t],", file=fw)
    print("\t\t},", file=fw)
