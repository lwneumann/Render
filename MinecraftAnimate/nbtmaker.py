from MinecraftAnimate.config import *
from MinecraftAnimate.nbt_structure_utils import NBTStructure, Vector, BlockData


def make_nbt(struct, name=DEFAULT_STRUCT_NAME):
    structure = NBTStructure()

    for y in range(len(struct)):
        for x in range(len(struct[0])):
            for z in range(len(struct[0][0])):
                structure.set_block(Vector(x, y, z), BlockData(struct[y][x][z]))

    structure.get_nbt().write_file(filename=f"{name}.nbt")
    return
