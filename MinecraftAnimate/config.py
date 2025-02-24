"""
NBTStructure().set_block(pos, block, inv, other_nbt)


from nbt_structure_utils import NBTStructure, Vector, Cuboid, BlockData

    nbtstructure = NBTStructure()
    c1, c2 = Vector(0, 0, 0), Vector(4, 4, 4)
    nbtstructure.fill(Cuboid(c1, c2), BlockData("stone"))
    nbtstructure.get_nbt().write_file(filename="hollow_box.nbt")

a =[["gold_block", "dirt", "sand"],
    ["stone", "glowstone", "obsidian"],
    ["bedrock", "coal_ore", "glass"]]


animate is always namespace, pack name can vary and mcmeta can change
"""

# # Settings
NAMESPACE = 'AnimateTest'
FPS = 30
SECONDS = 5
TOTAL_FRAMES = FPS * SECONDS
MIN_SPF = 0.025
FPS_FIG = 3

#      Y,   X,  Z
SIZE = 10, 10, 10

# # File Settings
STRUCTURE_FOLDER_PATH = f"./{NAMESPACE}/data/animate/structures/"
TEST_FOLDER_NAME = "./testStructs/"
BASE_PACK = "template_pack"

# # Structures
DEFAULT_STRUCT_NAME = "test"
