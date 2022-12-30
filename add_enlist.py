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
    SMACEnv = {
        "3s_vs_5z": {
            "MAT_pma": [
                "hlsong/SMAC_3s_vs_5z/qyct2efu",
                "hlsong/SMAC_3s_vs_5z/36pmh8ey",
                "hlsong/SMAC_3s_vs_5z/pn7qbmdm",
                "hlsong/SMAC_3s_vs_5z/w0idto6c",
                "hlsong/SMAC_3s_vs_5z/xw68btg8",
            ],
            "MAT_jpr": [
                "hlsong/SMAC_3s_vs_5z/hik9xqm8",
                "hlsong/SMAC_3s_vs_5z/11f23wkw",
                "hlsong/SMAC_3s_vs_5z/9idpu8tp",
            ],
            "MAT": [
                "hlsong/SMAC_3s_vs_5z/c9dko9qd",
                "hlsong/SMAC_3s_vs_5z/627s3vqi",
                "hlsong/SMAC_3s_vs_5z/a29fcu5e",
                "hlsong/SMAC_3s_vs_5z/74mmbxa8",
            ],
            "MAPPO_pma": [
                "hlsong/SMAC_3s_vs_5z/r5ivcjfe",
                "hlsong/SMAC_3s_vs_5z/0y0i9f4s",
                "hlsong/SMAC_3s_vs_5z/lvy01wll",
                "hlsong/SMAC_3s_vs_5z/jx9k6xcp",
            ],
            "MAPPO_jpr": [
                "hlsong/SMAC_3s_vs_5z/9ojx6178",
                "hlsong/SMAC_3s_vs_5z/3lhbogd8",
                "hlsong/SMAC_3s_vs_5z/yquw1f6f",
                "hlsong/SMAC_3s_vs_5z/3378ijsb",
                "hlsong/SMAC_3s_vs_5z/j8xu7auv",
                "hlsong/SMAC_3s_vs_5z/ikbi4ch3",
            ],
            "MAPPO": [
                "hlsong/SMAC_3s_vs_5z/59ndduec",
                "hlsong/SMAC_3s_vs_5z/k4j86761",
                "hlsong/SMAC_3s_vs_5z/u78prr79",
                "hlsong/SMAC_3s_vs_5z/w9vrqjf2",
                "hlsong/SMAC_3s_vs_5z/hzzpribt",
            ],
        },
        "mmm": {
            "MAT_pma": [
                "hlsong/SMAC_mmm/xv3u5rlz",
                "hlsong/SMAC_mmm/01i9mjbz",
                "hlsong/SMAC_mmm/6pbnyewy",
                "hlsong/SMAC_mmm/4ko7i25c",
                "hlsong/SMAC_mmm/keabdwo7",
                "hlsong/SMAC_mmm/jaxl3gd1",
            ],
            "MAT_jpr": [
                "hlsong/SMAC_mmm/er8naai4",
                "hlsong/SMAC_mmm/8dl9dyb4",
                "hlsong/SMAC_mmm/ri8qdp2n",
                "hlsong/SMAC_mmm/z7wfa6z9",
                "hlsong/SMAC_mmm/v4vdbn1a",
            ],
            "MAT": [
                "hlsong/SMAC_mmm/s887qbu3",
                "hlsong/SMAC_mmm/xd7mw701",
                "hlsong/SMAC_mmm/349vdxnl",
                "hlsong/SMAC_mmm/us3oflk5",
            ],
            "MAPPO_pma": [
                "hlsong/SMAC_mmm/wj53005z",
                "hlsong/SMAC_mmm/qnvkuxzc",
                "hlsong/SMAC_mmm/wpp5nxal",
                "hlsong/SMAC_mmm/dn6xf1az",
                "hlsong/SMAC_mmm/fx3bdybb",
            ],
            "MAPPO_jpr": [
                "hlsong/SMAC_mmm/xk8jv9da",
                "hlsong/SMAC_mmm/3ednpk1c",
                "hlsong/SMAC_mmm/11x4eqza",
                "hlsong/SMAC_mmm/ckqcujkq",
                "hlsong/SMAC_mmm/jwktx2ju",
            ],
            "MAPPO": [
                "hlsong/SMAC_mmm/inifsd94",
                "hlsong/SMAC_mmm/vlpmdrng",
                "hlsong/SMAC_mmm/bfxdoj32",
                "hlsong/SMAC_mmm/mqbx3jd6",
                "hlsong/SMAC_mmm/zrs9hem2",
            ],
        },
        "3s5z": {
            "MAT_pma": [
                "hlsong/SMAC_3s5z/owuh2a4v",
                "hlsong/SMAC_3s5z/mvj88nxq",
                "hlsong/SMAC_3s5z/ow2ytulu",
                "hlsong/SMAC_3s5z/gdbi6pvr",
                "hlsong/SMAC_3s5z/xlyoey3s",
            ],
            "MAT_jpr": [
                "hlsong/SMAC_3s5z/1mcij0rg",
                "hlsong/SMAC_3s5z/lb6f30ir",
                "hlsong/SMAC_3s5z/pcrlzavz",
                "hlsong/SMAC_3s5z/lf24yhlc",
                "hlsong/SMAC_3s5z/rnviip0r",
            ],
            "MAT": [
                "hlsong/SMAC_3s5z/gr4853f9",
                "hlsong/SMAC_3s5z/jozzqiub",
                "hlsong/SMAC_3s5z/9ufgh6x2",
                "hlsong/SMAC_3s5z/up22enyj",
                "hlsong/SMAC_3s5z/1mx1wbpi",
                "hlsong/SMAC_3s5z/jfqdzeil",
            ],
            "MAPPO_pma": [
                "hlsong/SMAC_3s5z/0hdbpfzj",
                "hlsong/SMAC_3s5z/bm878ffh",
                "hlsong/SMAC_3s5z/fyug206u",
                "hlsong/SMAC_3s5z/s0fmnwzu",
                "hlsong/SMAC_3s5z/1vp7rebt",
                "hlsong/SMAC_3s5z/310cpa5l",
                "hlsong/SMAC_3s5z/ycpkq1cd",
            ],
            "MAPPO_jpr": [
                "hlsong/SMAC_3s5z/my0desi6",
                "hlsong/SMAC_3s5z/bgwxf8nf",
                "hlsong/SMAC_3s5z/fu2a3sme",
            ],
            "MAPPO": [
                "hlsong/SMAC_3s5z/3mlje0my",
                "hlsong/SMAC_3s5z/jywwojyb",
                "hlsong/SMAC_3s5z/68os40nd",
                "hlsong/SMAC_3s5z/8gsky889",
                "hlsong/SMAC_3s5z/k4llsimf",
            ],
        },
    }
    env_list = {"mujoco": MujocoEnv, "StarCraft2": SMACEnv}
    return env_list


# if __name__ == "__main__":
#     project_name = "hlsong/mujoco_ant_8x1/"
#     with open("runlist.txt", "r") as f:
#         runlist = f.read().splitlines()
#         for run in runlist:
#             print(f"\"{project_name}{run}\",")
