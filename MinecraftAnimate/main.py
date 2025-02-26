from datetime import datetime
from alive_progress import alive_bar

from MinecraftAnimate.blockbase.blockbuilder import blockify

from MinecraftAnimate.nbtmaker import make_nbt
from MinecraftAnimate.datapack_maker import make_new_pack, populate_pack
from MinecraftAnimate.config import *


def render_datapack(step, pack_name=NAMESPACE, fps=FPS, seconds=SECONDS, uses_blockname=False, size=SIZE):
    total_frames = fps * seconds
    structure_path = f"./{pack_name}/data/animate/structures/"
    # Get time
    print(f'\n[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):-<76}-]')
    print('|' + ' '*78 + '|')

    # Make Pack
    print(f"{'--Preparing Datapack': <79}|")
    # - Make new datapack off template
    make_new_pack("./" + pack_name)
    populate_pack(FPS, size, pack_name)

    # Get Structures TODO
    past_colors = None
    state = None
    print('|' + ' '*78 + '|')
    print(f"{'--Rendering Structures': <79}|")
    with alive_bar(total_frames) as bar:
        for f in range(total_frames):
            state = step(f, state)
            # Check if input is alreay in blocknames or needs to be color mapped
            if uses_blockname:
                frame = state
            else:
                frame, past_colors = blockify(state, past_colors)
            # Make structure
            make_nbt(frame, name=structure_path+str(f))

            bar()

    print('|' + ' '*78 + '|')
    print(f'[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):->76}-]\n')
    return frame


if __name__ == "__main__":
    print('heyy :3')
