from datetime import datetime
from alive_progress import alive_bar

import blockbase.blockbuilder
import nbtmaker
import datapack_maker
from config import *


def render_datapack(scene, uses_blockname=False, size=SIZE):
    # Get time
    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):-<76}-]\n')

    # Make Pack
    print("---Preparing Datapack")
    # - Make new datapack off template
    datapack_maker.make_new_pack()
    datapack_maker.make_play(FPS)

    # Get Structures
    print('\n---Rendering Structures')
    with alive_bar(TOTAL_FRAMES) as bar:
        for f in range(TOTAL_FRAMES):
            state = scene.tick()
            # Check if input is alreay in blocknames or needs to be color mapped
            if uses_blockname:
                frame = state
            else:
                frame = blockbase.blockbuilder.blockify(state)
            nbtmaker.make_nbt(frame)
            bar()

    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):->76}-]\n')
    return


if __name__ == "__main__":
    print('heyy :3')
