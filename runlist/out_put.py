
from collections import defaultdict
from pathlib import Path
import wandb
api = wandb.Api(timeout=19)


def envlist():
    from .SMAC import SMACEnv
    from .mujoco import MujocoEnv
    env_list = {"mujoco": MujocoEnv, "StarCraft2": SMACEnv}
    return env_list


if __name__ == "__main__":
    env_name = "SMAC"
    var_name = "SMACEnv"
    map_names = ["3s_vs_5z", "mmm", "3s5z", "1c3s5z", "8m_vs_9m", "5m_vs_6m", "10m_vs_11m", "6h_vs_8z", "mmm2", "3s5z_vs_3s6z", "25m", "27m_vs_30m"]

    # env_name = "mujoco"
    # var_name = "MujocoEnv"
    # map_names = ["ant_4x2", "ant_8x1", "half_6x1", "half_3x2", "hopper_3x1", "swimmer_10x2", "walker-6x1", "walker_3x2"]

    # env_name = "Drones"
    # var_name = "DroneEnv"
    # map_names = ["flock", "flock_pid", "leader", "leader_pid"]
    update = True

    save_path = Path(f"./runlist/{env_name}.py")
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(str(save_path), "w+") as fw:
        print(f"{var_name} = {{", file=fw)
    for map_name in map_names:
        update = True
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
            if run.config["wandb_tag"] != "plot":
                run.config["wandb_note"] = "plot"
                run.config["wandb_tag"] = "plot"
                run.update()
            dic[algo].append(run.id)
        # save_path = Path(f"./runlist/{env_name}_{map_name}.txt")
        # save_path.parent.mkdir(parents=True, exist_ok=True)
        # with open(f"{str(save_path)}", "w") as fw:
        with open(str(save_path), "a+") as fw:
            print(" "*4+f"\"{map_name}\": {{", file=fw)
            for key in order_key:
                print(" "*8+f"\"{algo_name[key]}\": [", file=fw)
                for run in dic[key]:
                    print(" "*12+f"\"{project}/{run}\",", file=fw)
                print(" "*8+"],", file=fw)
            print(" "*4+"},", file=fw)
    with open(str(save_path), "a+") as fw:
        print(f"}}", file=fw)
