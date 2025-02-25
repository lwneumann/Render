import os
import shutil

from config import *

"""
This needs to make

Create a newly named folder for the datapack then add
- [namespace]: play.mcfunction
-> schedule fps
-> all if for frames
"""


def make_new_pack(pack_name=NAMESPACE):
    try:
        # Copy over
        files = os.listdir(BASE_PACK)
        shutil.copytree(BASE_PACK, pack_name)
    except shutil.Error as e:
        print(f"Error: {e}")
    except OSError as e:
        print(f"Error: {e}")
    return


def make_mcfunct(content, name):
    extension = "mcfunction"
    new_file = open(f'{name}.{extension}', 'w+')
    new_file.write(content)
    new_file.close()
    return


def make_json(name, values=[]):
    """
    r string
    """
    # Open
    extension = ".json"
    new_file = open(f'{name}.{extension}', 'w+')

    # Write values (pretty much just)
    start = r'{"values":['
    content = start
    for v in values:
        content += f"animate:{v},"
    end = r"]}"
    content += end

    new_file.write(content)
    new_file.close()
    return


def make_play(fps, name_space=NAMESPACE):
    path = f"./{name_space}/data/animate/functions/"

    spf = max(round(1 / fps, FPS_FIG), MIN_SPF)
    if spf == MIN_SPF:
        print("- ! Capping FPS at 40 (0.025 spf) !")
    # Setup
    content = f"""
# Places frames and increments frame count. Scheduled at FPS?
execute store result storage minecraft:frames input.frame int 1 run scoreboard players get @e[tag=projector,limit=1] frame_count
function animate:place_frame with storage minecraft:frames input
execute at @e[tag=projector] run scoreboard players add @e[tag=projector] frame_count 1

schedule function animate:play {spf}s"""

    make_mcfunct(content, path + "play")
    print("-Pack setup at\n", path+"play")
    return
