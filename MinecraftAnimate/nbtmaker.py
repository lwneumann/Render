from MinecraftAnimate.config import *
from MinecraftAnimate.nbt_structure_utils import NBTStructure, Vector, BlockData


def make_nbt(struct, name):
    structure = NBTStructure()

    # Make sure the structure is actually at the spot you want
    # Otherwise it will recenter automatically
    structure.set_block(Vector(0, 0, 0), BlockData("structure_void"))

    for y in range(len(struct)):
        for x in range(len(struct[0])):
            for z in range(len(struct[0][0])):
                if struct[y][x][z] != "structure_void":
                    structure.set_block(Vector(x, y, z), BlockData(struct[y][x][z]))

    structure.get_nbt().write_file(filename=f"{name}.nbt")
    return


def make_air(size, path):
    make_nbt([[['air' for z in range(size[2])] for x in range(size[1])] for y in range(size[0])], path+'clear')
    return
