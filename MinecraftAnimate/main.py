from datetime import datetime
from alive_progress import alive_bar

from MinecraftAnimate.blockbase.blockbuilder import blockify

from MinecraftAnimate.nbtmaker import make_nbt
from MinecraftAnimate.datapack_maker import make_new_pack, populate_pack
from MinecraftAnimate.config import *


def render_datapack(scene, pack_name=NAMESPACE, fps=FPS, seconds=SECONDS, uses_blockname=False, size=SIZE):
    total_frames = fps * seconds
    structure_path = f"./{NAMESPACE}/data/animate/structures/"
    # Get time
    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):-<76}-]\n')

    # Make Pack
    print("---Preparing Datapack")
    # - Make new datapack off template
    make_new_pack("./" + pack_name)
    populate_pack(FPS, pack_name)

    # Get Structures TODO
    print('\n---Rendering Structures')
    with alive_bar(total_frames) as bar:
        for f in range(total_frames):
            state = scene.step()
            # Check if input is alreay in blocknames or needs to be color mapped
            if uses_blockname:
                frame = state
            else:
                frame = blockify(state)
            make_nbt(frame, name=structure_path+str(f))
            bar()

    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):->76}-]\n')
    return


if __name__ == "__main__":
    print('heyy :3')
