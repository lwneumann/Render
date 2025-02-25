from datetime import datetime
from alive_progress import alive_bar

import blockbase.blockbuilder
import nbtmaker
import datapack_maker
from config import *


def render_datapack(scene, pack_name=NAMESPACE, fps=FPS, seconds=SECONDS, uses_blockname=False, size=SIZE):
    total_frames = fps * seconds
    structure_path = f"./{NAMESPACE}/data/animate/structures/"
    # Get time
    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):-<76}-]\n')

    # Make Pack
    print("---Preparing Datapack")
    # - Make new datapack off template
    datapack_maker.make_new_pack(pack_name)
    datapack_maker.make_play(FPS, pack_name)

    # Get Structures TODO
    print('\n---Rendering Structures')
    with alive_bar(total_frames) as bar:
        for f in range(total_frames):
            state = scene.step()
            # Check if input is alreay in blocknames or needs to be color mapped
            if uses_blockname:
                frame = state
            else:
                frame = blockbase.blockbuilder.blockify(state)
            nbtmaker.make_nbt(frame, name=structure_path+str(f))
            bar()

    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):->76}-]\n')
    return


if __name__ == "__main__":
    print('heyy :3')
