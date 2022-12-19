import pandas as pd
import wandb
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib.pyplot import MultipleLocator
api = wandb.Api(timeout=19)

project = "hlsong/mujoco_ant_4x2"
# runs = api.runs(project , {"$and": [{"config.algorithm_name": 'mat'},]})
runs = api.runs(project, {"$and": [{"config.algorithm_name": 'mappo_maska'}, ]}, order="-created_at")

for run in runs:
    config = {k: v for k, v in run.config.items() if not k.startswith('_')}
    if 'use_action_loss' not in run.config.keys():
        print(run.name)
        run.config["use_action_loss"] = False
    run.update()
