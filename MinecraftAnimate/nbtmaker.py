from MinecraftAnimate.config import *
from MinecraftAnimate.nbt_structure_utils import NBTStructure, Vector, BlockData


def make_nbt(struct, name):
    structure = NBTStructure()

    for y in range(len(struct)):
        for x in range(len(struct[0])):
            for z in range(len(struct[0][0])):
                if struct[y][x][z] != "structure_void":
                    structure.set_block(Vector(x, y, z), BlockData(struct[y][x][z]))

    structure.get_nbt().write_file(filename=f"{name}.nbt")
    return


def make_air(size, path):
    make_nbt([[['air' for z in range(len(size[1]))] for x in range(len(size[0]))] for y in range(len(size))], path+'clear')
    return
