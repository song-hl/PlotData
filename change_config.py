import pandas as pd
import wandb
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib.pyplot import MultipleLocator
api = wandb.Api(timeout=19)

project = "hlsong/SMAC_2"
# runs = api.runs(project , {"$and": [{"config.algorithm_name": 'mat'},]})
runs = api.runs(project, {"$and": [{"config.algorithm_name": 'mat_mask'}, ]}, order="-created_at")

for run in runs:
    config = {k: v for k, v in run.config.items() if not k.startswith('_')}
    # if 'maska_type' not in run.config.keys():
    print(run.name)
    run.config["maska_jumps"] = 2
    run.update()
