def envlist():
    MujocoEnv = {
        "Ant-8x1-obsk=1": {
            "MAPPO_MaskAgengt": [  # N(0,1)
                "hlsong/mujoco_ant_8x1/emdsblf8",
                "hlsong/mujoco_ant_8x1/uyl7lhrs",
                "hlsong/mujoco_ant_8x1/kkqx8rzu",
                "hlsong/mujoco_ant_8x1/fbrskzrt",
            ],
            # "MAPPO_MaskAgengt": [ # zero
            #     "hlsong/mujoco_ant_8x1/msor4jj7",
            #     "hlsong/mujoco_ant_8x1/s99psjfo",
            #     "hlsong/mujoco_ant_8x1/1iff8grs",
            #     "hlsong/mujoco_ant_8x1/n2vzvyvk",
            # ],
            "MAPPO": [
                "hlsong/mujoco_ant_8x1/jt1al8zh",
                "hlsong/mujoco_ant_8x1/u12rp84s",
                "hlsong/mujoco_ant_8x1/lpqz3bjr",
                "hlsong/mujoco_ant_8x1/sw2fg4gw",
                "hlsong/mujoco_ant_8x1/6kbqtc2t",
            ],
        },
        # "Ant-8x1-obsk=0": {
        #     "MAPPO_MaskAgengt N(0,1)": [ # N(0,1)
        #         "hlsong/mujoco_ant_8x1/sncqjfc7",
        #         "hlsong/mujoco_ant_8x1/l6fdmui1",
        #         "hlsong/mujoco_ant_8x1/w8lpljnj",
        #         "hlsong/mujoco_ant_8x1/vk170yuy",
        #         "hlsong/mujoco_ant_8x1/bvao3gvb",
        #     ],
        #     "MAPPO_MaskAgengt zero": [ # zero
        #         "hlsong/mujoco_ant_8x1/xlsnwtmn",
        #         "hlsong/mujoco_ant_8x1/kvfw96ju",
        #         "hlsong/mujoco_ant_8x1/7b1tjrzc",
        #         "hlsong/mujoco_ant_8x1/e8cgoaz0",
        #         "hlsong/mujoco_ant_8x1/32j165ts",
        #         "hlsong/mujoco_ant_8x1/lasy69hs",
        #     ],
        #     "MAPPO ": [
        #         "hlsong/mujoco_ant_8x1/j11o94a2",
        #         "hlsong/mujoco_ant_8x1/rdmojjpx",
        #         "hlsong/mujoco_ant_8x1/5gvvintq",
        #         "hlsong/mujoco_ant_8x1/v444woxb",
        #         "hlsong/mujoco_ant_8x1/qv957j41",
        #     ],
        # },
        "Walker-6x1-obsk=1": {  
            "MAPPO_MaskAgengt": [  # zero
                "hlsong/mujoco_walker-6x1/f0t6sbl3",
                "hlsong/mujoco_walker-6x1/fizkvhkl",
                "hlsong/mujoco_walker-6x1/olke5aw7",
                "hlsong/mujoco_walker-6x1/sqiaid51",
                "hlsong/mujoco_walker-6x1/3riqslxu",
                "hlsong/mujoco_walker-6x1/d4mzt00q",
            ],
            "MAPPO": [
                "hlsong/mujoco_walker-6x1/y4rruo1l",
                "hlsong/mujoco_walker-6x1/5v5g8e0j",
                "hlsong/mujoco_walker-6x1/vk06o4s5",
                "hlsong/mujoco_walker-6x1/f7h9hlq3",
                "hlsong/mujoco_walker-6x1/ipgphsb2",
            ],
        },
        "Half_cheetah-6x1-obsk=0": {
            "MAPPO_MaskAgengt": [  # zero
                "hlsong/mujoco_half/24btbxxc",
                "hlsong/mujoco_half/e8r1qccg",
                "hlsong/mujoco_half/npdwxhej",
                "hlsong/mujoco_half/qjtdbt0x",
                "hlsong/mujoco_half/qz0j0jlj",
            ],
            "MAPPO": [
                "hlsong/mujoco_half/fw00zacg",
                "hlsong/mujoco_half/2t179d49",
                "hlsong/mujoco_half/ozeti4ej",
                "hlsong/mujoco_half/k7qpr02u",
                "hlsong/mujoco_half/e5sn0w3w",
            ],
        },
        "Half_cheetah-6x1-obsk=1": {
            "MAPPO_MaskAgengt": [  # zero
                "hlsong/mujoco_half/ju4ouhr4",
                "hlsong/mujoco_half/ysnznu56",
                "hlsong/mujoco_half/xwnpuha6",
                "hlsong/mujoco_half/0mpw1yn2",
                "hlsong/mujoco_half/obijgl83",
                "hlsong/mujoco_half/8yiggy0z",
            ],
            "MAPPO": [
                "hlsong/mujoco_half/e9wg2ay1",
                "hlsong/mujoco_half/ceopgew2",
                "hlsong/mujoco_half/xmvtketa",
                "hlsong/mujoco_half/s916d01w",
                "hlsong/mujoco_half/lr075x9t",
            ],
        },
        "Hopper-3x1-obsk=1": {
            "MAPPO_MaskAgengt ": [  # N(0,1) sota
                "hlsong/mujoco_hopper/p6tvc4ir",
                "hlsong/mujoco_hopper/3df81ork",
                "hlsong/mujoco_hopper/6qhlrspb",
            ],
            # "MAPPO_MaskAgengt": [  # zero
            #     "hlsong/mujoco_hopper/vhm55u18",
            #     "hlsong/mujoco_hopper/u4xul9tc",
            #     "hlsong/mujoco_hopper/c04m5wpp",
            #     "hlsong/mujoco_hopper/kfdbb6e2",
            # ],
            "MAPPO": [
                "hlsong/mujoco_hopper/j2ay49u7",
                "hlsong/mujoco_hopper/w8qibrvs",
                "hlsong/mujoco_hopper/26guw3ci",
                "hlsong/mujoco_hopper/dxcc4xgu",
                "hlsong/mujoco_hopper/r9y37xnu",
            ],
        },
        "Ant-4x2-obsk=1": {
            "MAPPO_MaskAgengt": [  # zero # smooth = 7
                "hlsong/mujoco_ant_4x2/74gfdtzu",
                "hlsong/mujoco_ant_4x2/fdvkr9ea",
                "hlsong/mujoco_ant_4x2/x9tpib42",
                "hlsong/mujoco_ant_4x2/tzctdn1x",
            ],
            "MAPPO": [
                "hlsong/mujoco_ant_4x2/b72xwrz3",
                "hlsong/mujoco_ant_4x2/9le8r0vi",
                "hlsong/mujoco_ant_4x2/k18rxeqq",
                "hlsong/mujoco_ant_4x2/o3vtg89g",
                "hlsong/mujoco_ant_4x2/p8ba9ilv",
                "hlsong/mujoco_ant_4x2/pi0xk37a",
            ],
        },
        "Walker-3x2-obsk=1": {
            "MAPPO_MaskAgengt": [  # zero # smooth = 7
                "hlsong/mujoco_walker_3x2/jp46a4an",
                "hlsong/mujoco_walker_3x2/ukf8jg8w",
                "hlsong/mujoco_walker_3x2/63jljv3b",
                "hlsong/mujoco_walker_3x2/31iknwu4",
                "hlsong/mujoco_walker_3x2/41my7o9x",
            ],
            "MAPPO": [
                "hlsong/mujoco_walker_3x2/g99j68c2",
                "hlsong/mujoco_walker_3x2/svcazprs",
                "hlsong/mujoco_walker_3x2/dv3d45uo",
                "hlsong/mujoco_walker_3x2/9c4owawz",
                "hlsong/mujoco_walker_3x2/v5kjuz9t",
                "hlsong/mujoco_walker_3x2/eobqir0c",
            ],
        },
        "Half_cheetah-3x2-obsk=1": {
            "MAPPO_MaskAgengt": [  # zero # smooth = 7
                "hlsong/mujoco_half_3x2/ldhsswxm",
                "hlsong/mujoco_half_3x2/1vatv294",
                "hlsong/mujoco_half_3x2/fk9hs9b5",
                "hlsong/mujoco_half_3x2/oejq874n",
                "hlsong/mujoco_half_3x2/q7zz2sym",
                "hlsong/mujoco_half_3x2/wagbou9c",
            ],
            "MAPPO": [
                # "hlsong/mujoco_half_3x2/skayz5fv",
                "hlsong/mujoco_half_3x2/zababmbw",
                "hlsong/mujoco_half_3x2/5wvtemez",
                "hlsong/mujoco_half_3x2/huyp1bnm",
                "hlsong/mujoco_half_3x2/gjmfcsl3",
                # "hlsong/mujoco_half_3x2/tt4glc2k",
            ],
        },
        "Swimmer-6x1-obsk=1": {
            "MAPPO_MaskAgengt": [  # zero # smooth = 7
                "hlsong/mujoco_swimmer/6luzm22v",
                "hlsong/mujoco_swimmer/qmhowdur",
                "hlsong/mujoco_swimmer/7ssoucly",
                "hlsong/mujoco_swimmer/uyrrym6q",
                "hlsong/mujoco_swimmer/jzumdpke",
            ],
            "MAPPO": [
                "hlsong/mujoco_swimmer/g0en7qfd",
                "hlsong/mujoco_swimmer/mwcvpnw5",
                "hlsong/mujoco_swimmer/v2cs08j4",
                "hlsong/mujoco_swimmer/qzqk3qrm",
                "hlsong/mujoco_swimmer/bp2gvo3w",
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
