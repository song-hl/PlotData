import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import numpy as np
import argparse
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

DIV_LINE_WIDTH = 50


def plot_data(data, xaxis='Step', value="AvgEpRet", condition="Condition1", smooth=1, ax=None, colors=None, **kwargs):
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
    # sns.set(style="darkgrid", palette="deep", font_scale=1.5)
    # ax.margins(0.05)
    sns.tsplot(data=data, time=xaxis, value=value, unit="Unit", legend=True, color=colors,
               condition=condition, ci='sd', ax=ax, linewidth=2.5, **kwargs)
    """
    If you upgrade to any version of Seaborn greater than 0.8.1, switch from
    tsplot to lineplot replacing L29 with:
        sns.lineplot(data=data, x=xaxis, y=value, hue=condition, ci='sd', **kwargs)
    Changes the colorscheme and the default legend style, though.
    """

    xscale = np.max(np.asarray(data[xaxis])) > 5e3
    if xscale:
        # Just some formatting niceness: x-axis scale in scientific notation if max x is large
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    yscale = np.max(np.asarray(data[value])) > 5e4
    if yscale:
        # Just some formatting niceness: x-axis scale in scientific notation if max x is large
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    # ax.tight_layout(pad=0.5)


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


def get_datasets(logdir, legend=None, tag=None, data_file='progress.txt'):
    """
    Recursively look through logdir for output files produced by
    spinup.logx.Logger.
    Assumes that any file "progress.txt" is a valid hit.
    """
    datasets = []
    units = dict()
    exp_idx = 0
    for root, _, files in os.walk(logdir):
        if ('progress.txt' in files) or ('progress.csv' in files):
            exp_name = None
            try:
                config_path = open(os.path.join(root, 'config.json'))
                config = json.load(config_path)
                if tag in config:
                    exp_name = config[tag]
            except:
                print('No file named config.json')
            condition1 = legend or exp_name
            condition2 = condition1 + '-' + str(exp_idx)
            exp_idx += 1
            if condition1 not in units:
                units[condition1] = 0
            unit = units[condition1]
            units[condition1] += 1

            try:
                if 'progress.txt' in files:
                    exp_data = pd.read_table(
                        os.path.join(root, 'progress.txt'))
                elif 'progress.csv' in files:
                    exp_data = pd.read_csv(os.path.join(root, 'progress.csv'))
            except:
                print('Could not read from %s' %
                      os.path.join(root, data_file))
                continue
            if exp_data.shape[0] > 1000:
                exp_data = exp_data[::20][1:]
            exp_data.insert(len(exp_data.columns), 'Unit', unit)
            exp_data.insert(len(exp_data.columns), 'Condition1', condition1)
            exp_data.insert(len(exp_data.columns), 'Condition2', condition2)
            datasets.append(exp_data)
    return datasets, units, condition1


def main(args):
    envs = [
        'Alien', 'Amidar', 'Assault', 'Asterix', 'Asteroids', 'Atlantis',
        'BankHeist', 'BattleZone', 'BeamRider', 'Bowling', 'Boxing', 'Breakout',
        'Centipede', 'ChopperCommand', 'CrazyClimber', 'DemonAttack', 'DoubleDunk', 'Enduro',
        'FishingDerby', 'Freeway', 'Frostbite', 'Gopher', 'Gravitar', 'IceHockey',
        'Jamesbond', 'Kangaroo', 'Krull', 'KungFuMaster', 'MontezumaRevenge', 'MsPacman',
        'NameThisGame', 'Pitfall', 'Pong', 'PrivateEye', 'Qbert', 'Riverraid',
        'RoadRunner', 'Robotank', 'Seaquest', 'SpaceInvaders', 'StarGunner', 'Tennis',
        'TimePilot', 'Tutankham', 'UpNDown', 'Venture', 'VideoPinball', 'WizardOfWor', 'Zaxxon'
    ]
    algs = ['PPO_test_10M_10seed']
    legends = ['PPO ours']
    colors = None
    # colors = ['gray', 'green', 'red', 'blue']
    version = 'NoFrameskip-v4'

    nsize = (10, 5)

    sns.set(style="darkgrid", palette="deep", font_scale=1.5)
    fig, axis = plt.subplots(nrows=nsize[0], ncols=nsize[1],
                             figsize=(6.4*nsize[1], 4.8*nsize[0]*1.1))

    for i in range(len(envs)):
        env_name = envs[i] + version
        base_dir = os.path.join(args.logdir, env_name)
        if not os.path.exists(base_dir):
            raise ValueError(f'No such basedir: {base_dir}')

        # Check whether the logdirs are valid.
        logdirs = []
        for alg in algs:
            alg_dir = os.path.join(base_dir, alg)
            if os.path.isdir(alg_dir):
                logdirs += [alg_dir]
            else:
                raise ValueError(f'No such algdir: {alg_dir}')

        # legend and logdir must be corresponding.
        if legends:
            assert len(legends) == len(logdirs)

        print('Getting data from...\n' + '='*DIV_LINE_WIDTH + '\n')

        data = []
        for logdir, legend in zip(logdirs, legends):
            datasets, units, cond = get_datasets(
                logdir=logdir, legend=legend, tag=args.tag, data_file=args.file)
            data += datasets
            print(f'{logdir} -> {cond}, {units[cond]}')

        print('\n' + '='*DIV_LINE_WIDTH)
        print('Plotting...')

        # Choose which subplot to plot
        ax = axis[i // nsize[1], i % nsize[1]]

        condition = 'Condition2' if args.count else 'Condition1'
        plot_data(data, xaxis=args.xaxis, value=args.value, condition=condition,
                  smooth=args.smooth, ax=ax, colors=colors)

        ax.set_title(envs[i])
        ax.set_xlabel('')
        ax.set_ylabel('')

        def mappingx(x, pos): 
            return (x / 1e6)

        # ax.xaxis.set_major_formatter(ticker.EngFormatter())
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mappingx))

        ax.autoscale()
        ax.set_box_aspect(4.8/6.4)
        ax.legend(loc='best')

    # set labels
    for ax in axis[-1, :]:
        ax.set_xlabel('Steps(M)', labelpad=10)
    for ax in axis[:, 0]:
        ax.set_ylabel('Average Performance', labelpad=10)

    axis[-1][-1].remove()  # don't display empty ax

    plt.tight_layout(pad=0.5)
    # lines = fig.axes[-1].get_lines()
    # # for line in lines:
    # #     line.set_linewidth(2.0)
    # handles = [mpatches.Patch(color=line.get_c(), label=legend)
    #            for (line, legend) in zip(lines, legends)]
    # fig.legend(handles=handles, loc='lower center', prop={'size': 25},
    #            ncol=len(algs), handlelength=1, borderaxespad=0.)
    # plt.subplots_adjust(bottom=0.1)
    plt.show()
    plt.savefig('all.pdf')
    plt.savefig('all.svg')
    print(f"Saved into {os.path.abspath('all.pdf')}")


"""
Usage:
    python rl-exercise/lib/utils/plot.py --logdir data/bench_dqn
    data/bench_ddqn data/bench_dueling --xaxis Iteration --value Value
    --smooth 8 --tag exp_name --legend my_dqn my_ddqn my_dueling
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', required=True, type=str)
    parser.add_argument('--legend', '-l', default=None, nargs='*')
    parser.add_argument('--xaxis', '-x', default='Step')
    parser.add_argument('--value', '-y', default='AvgEpRet')
    parser.add_argument('--smooth', '-s', type=int, default=1)
    parser.add_argument('--tag', type=str, default='exp_name')
    parser.add_argument('--file', type=str, default='progress.txt')
    parser.add_argument('--count', action='store_true')
    parser.add_argument('--name', type=str, default='exp')
    args = parser.parse_args()
    main(args)
