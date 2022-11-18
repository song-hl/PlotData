def envlist():
    MujocoEnv = {
        "Ant-8x1-obsk=1": {
            "MAPPO_MaskAgengt N(0,1)": [
                "hlsong/mujoco_ant_8x1/emdsblf8",
                "hlsong/mujoco_ant_8x1/uyl7lhrs",
                "hlsong/mujoco_ant_8x1/kkqx8rzu",
                "hlsong/mujoco_ant_8x1/fbrskzrt",
            ],
            "MAPPO_MaskAgengt zero": [
                "hlsong/mujoco_ant_8x1/msor4jj7",
                "hlsong/mujoco_ant_8x1/s99psjfo",
                "hlsong/mujoco_ant_8x1/1iff8grs",
                "hlsong/mujoco_ant_8x1/n2vzvyvk",
            ],
            "MAPPO": [
                "hlsong/mujoco_ant_8x1/jt1al8zh",
                "hlsong/mujoco_ant_8x1/u12rp84s",
                "hlsong/mujoco_ant_8x1/lpqz3bjr",
                "hlsong/mujoco_ant_8x1/sw2fg4gw",
                "hlsong/mujoco_ant_8x1/6kbqtc2t",
            ],
        },
        "Ant-8x1-obsk=0": {
            "MAPPO_MaskAgengt N(0,1)": [
                "hlsong/mujoco_ant_8x1/sncqjfc7",
                "hlsong/mujoco_ant_8x1/l6fdmui1",
                "hlsong/mujoco_ant_8x1/w8lpljnj",
                "hlsong/mujoco_ant_8x1/vk170yuy",
                "hlsong/mujoco_ant_8x1/bvao3gvb",
            ],
            "MAPPO_MaskAgengt zero": [
                "hlsong/mujoco_ant_8x1/xlsnwtmn",
                "hlsong/mujoco_ant_8x1/kvfw96ju",
                "hlsong/mujoco_ant_8x1/7b1tjrzc",
                "hlsong/mujoco_ant_8x1/e8cgoaz0",
                "hlsong/mujoco_ant_8x1/32j165ts",
                "hlsong/mujoco_ant_8x1/lasy69hs",
            ],
            "MAPPO ": [
                "hlsong/mujoco_ant_8x1/j11o94a2",
                "hlsong/mujoco_ant_8x1/rdmojjpx",
                "hlsong/mujoco_ant_8x1/5gvvintq",
                "hlsong/mujoco_ant_8x1/v444woxb",
                "hlsong/mujoco_ant_8x1/qv957j41",
            ],
        },
        "LeaderFollower-4xagent": {
            "MAT": [
                "hlsong/drone_flock/6f515t5e",
                "hlsong/drone_flock/49dki36q",
                "hlsong/drone_flock/tbabd3ph",
                "hlsong/drone_flock/zqt3wabq",
                "hlsong/drone_flock/9pz6r54v",
                "hlsong/drone_flock/lhwte7je",
            ],
            "MASK_AGENT": [
                "hlsong/drone_flock/34l4scr8",
                "hlsong/drone_flock/7m83f190",
                "hlsong/drone_flock/ssm6oaoy",
                "hlsong/drone_flock/2yebjpm7",
            ],
            "MASK_AGENT_pro": [
                "hlsong/drone_flock/0sozqzjq",
                "hlsong/drone_flock/uhflgrpf",
                "hlsong/drone_flock/shit0ewx",
                "hlsong/drone_flock/h7ivvza2",
                "hlsong/drone_flock/4j1wcvho",
            ],
        },
        "Meetup-4xagent": {
            "MAT": [
                "hlsong/drone_flock/6f515t5e",
                "hlsong/drone_flock/49dki36q",
                "hlsong/drone_flock/tbabd3ph",
                "hlsong/drone_flock/zqt3wabq",
                "hlsong/drone_flock/9pz6r54v",
                "hlsong/drone_flock/lhwte7je",
            ],
            "MASK_AGENT": [
                "hlsong/drone_flock/34l4scr8",
                "hlsong/drone_flock/7m83f190",
                "hlsong/drone_flock/ssm6oaoy",
                "hlsong/drone_flock/2yebjpm7",
            ],
            "MASK_AGENT_pro": [
                "hlsong/drone_flock/0sozqzjq",
                "hlsong/drone_flock/uhflgrpf",
                "hlsong/drone_flock/shit0ewx",
                "hlsong/drone_flock/h7ivvza2",
                "hlsong/drone_flock/4j1wcvho",
            ],
        },
    }
    env_list = {"mujoco": MujocoEnv}
    return env_list


# if __name__ == "__main__":
#     project_name = "hlsong/mujoco_ant_8x1/"
#     with open("runlist.txt", "r") as f:
#         runlist = f.read().splitlines()
#         for run in runlist:
#             print(f"\"{project_name}{run}\",")
