import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import numpy as np
import argparse
from matplotlib.ticker import EngFormatter
import matplotlib.ticker as ticker

from pathlib import Path

DIV_LINE_WIDTH = 50


def plot_data(data, xaxis='Step', value="AvgEpRet", condition="Condition1", smooth=1, ax=None, **kwargs):
    if smooth > 1:
        """
        smooth data with moving window average.
        that is,
            smoothed_y[t] = average(y[t-k], y[t-k+1], ..., y[t+k-1], y[t+k])
        where the "smooth" param is width of that window (2k+1)
        """
        y = np.ones(smooth)
        for datum in data:
            x = np.asarray(datum[value])  # (200, 1)
            x = np.squeeze(x)  # (200,)
            z = np.ones(len(x))
            smoothed_x = np.convolve(x, y, 'same') / np.convolve(z, y, 'same')
            datum[value] = smoothed_x

    if isinstance(data, list):
        data = pd.concat(data, ignore_index=True)
    sns.lineplot(data=data, x=xaxis, y=value, hue=condition, ci='sd', **kwargs)

    xscale = np.max(np.asarray(data[xaxis])) > 5e3
    if xscale:
        # Just some formatting niceness: x-axis scale in scientific notation if max x is large
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    plt.tight_layout(pad=0.5)


"""
Iteraion    Value   Unit    Condition
..          ..      0       dqn
..          ..      1       dqn
..          ..      2       dqn
..          ..      3       dqn
..          ..      4       dqn
..          ..      0       ddqn
..          ..      1       ddqn
..          ..      2       ddqn
..          ..      3       ddqn
..          ..      4       ddqn
..          ..      0       duel
..          ..      1       duel
..          ..      2       duel
..          ..      3       duel
..          ..      4       duel
"""


def get_datasets(logdir, legend=None, data_type='csv'):
    """
    Recursively look through logdir for output files produced by
    spinup.logx.Logger.
    Assumes that any file "progress.txt" is a valid hit.
    """
    datasets = []
    units = dict()
    exp_idx = 0

    logdir = Path.cwd() / logdir
    if data_type == 'csv':
        for files in logdir.rglob('*.csv'):
            print(files)
            exp_name = None
            condition1 = legend or exp_name
            condition2 = condition1 + '-' + str(exp_idx)
            exp_idx += 1
            if condition1 not in units:
                units[condition1] = 0
            unit = units[condition1]
            units[condition1] += 1
            exp_data = pd.read_csv(files)
            exp_data.insert(len(exp_data.columns), 'Unit', unit)
            exp_data.insert(len(exp_data.columns), 'Condition1', condition1)
            exp_data.insert(len(exp_data.columns), 'Condition2', condition2)
            datasets.append(exp_data)
    elif data_type == 'txt':
        for files in logdir.rglob('*.txt'):
            print(files)
            exp_name = None
            condition1 = legend or exp_name
            condition2 = condition1 + '-' + str(exp_idx)
            exp_idx += 1
            if condition1 not in units:
                units[condition1] = 0
            unit = units[condition1]
            units[condition1] += 1
            exp_data = pd.read_table(files)
            exp_data.insert(len(exp_data.columns), 'Unit', unit)
            exp_data.insert(len(exp_data.columns), 'Condition1', condition1)
            exp_data.insert(len(exp_data.columns), 'Condition2', condition2)
            datasets.append(exp_data)
    return datasets, units, condition1


def main(args):
    # Check whether the logdirs are valid.
    logdirs = []
    for logdir in args.logdir:
        if os.path.isdir(logdir):
            logdirs += [logdir]
        else:
            raise ValueError(f'No such directory: {logdir}')

    # legend and logdir must be corresponding.
    if args.legend:
        assert len(args.legend) == len(logdirs)

    print('Getting data from...\n' + '='*DIV_LINE_WIDTH + '\n')

    data = []
    if args.legend:
        for logdir, legend in zip(logdirs, args.legend):
            datasets, units, cond = get_datasets(
                logdir=logdir, legend=legend)
            data += datasets
            print(f'{logdir} -> {cond}, {units[cond]}')
    else:
        for logdir in logdirs:
            datasets, units, cond = get_datasets(
                logdir=logdir, tag=args.tag, data_file=args.file)
            data += datasets
            print(f'{logdir} -> {cond}, {units[cond]}')

    print('\n' + '='*DIV_LINE_WIDTH)
    print('Plotting...')

    sns.set(style="darkgrid", font_scale=1.8)
    sns.set_palette('husl', 8, .75)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.4*1.5, 4.8*1.5))
    plt.title(args.name)
    condition = 'Condition2' if args.count else 'Condition1'
    plot_data(data, xaxis=args.xaxis, value=args.value, condition=condition, smooth=args.smooth, ax=ax)

    ax.set_xlabel('Steps(M)', labelpad=10)
    ax.set_ylabel('Reward', labelpad=10)
    def mappingx(x, pos): 
        return (x / 1e6)
    # ax.xaxis.set_major_formatter(ticker.EngFormatter())
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mappingx))
    ax.legend(loc='best')
    # ax.set(ylim=(0, 0.03))
    ax.autoscale()

    plt.show()
    plt.savefig(f'{args.name}.pdf')
    print(f"Saved into {os.path.abspath(f'{args.name}.pdf')}")


"""
Usage:
    python rl-exercise/lib/utils/plot.py --logdir data/bench_dqn
    data/bench_ddqn data/bench_dueling --xaxis Iteration --value Value
    --smooth 8 --tag exp_name --legend my_dqn my_ddqn my_dueling
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', required=True, nargs='*')
    parser.add_argument('--legend', '-l', default=None, nargs='*')
    parser.add_argument('--xaxis', '-x', default='Iteration')
    parser.add_argument('--value', '-y', default='Value')
    parser.add_argument('--smooth', '-s', type=int, default=1)
    parser.add_argument('--tag', type=str, default='exp_name')
    parser.add_argument('--file', type=str, default='progress.txt')
    parser.add_argument('--count', action='store_true')
    parser.add_argument('--name', type=str, default='exp')
    args = parser.parse_args()
    main(args)
