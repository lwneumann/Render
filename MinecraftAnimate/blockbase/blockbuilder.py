from MinecraftAnimate.blockbase.blockcolors import *


def dist(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def get_block_from_color(color):
    if color == None:
        return "structure_void"

    block = None
    # Max distance is around 441.
    # |
    # V
    score = 450
    for b in BLOCK_COLOR:
        bd = dist(color, b[1])
        if bd < score:
            block = b[0]
            score = bd
    return block


def get_grey_block(r, g, b):
    # Simple 4 tone greyscale mapping
    intensity = (r + g + b) // 3
    quarter = 63.75 # 255/4
    block = "minecraft:"
    if intensity < quarter:
        block += "white_concrete"
    elif intensity < quarter*2:
        block += "light_gray_concrete"
    elif intensity < quarter*3:
        block += "gray_concrete"
    else:
        block += "black_concrete"
    return block


def blockify(structure, seen_colors=None):
    """
    y
    |
    /\
    x z

    [ y slices
        [ [ z ] x ]
    ]
    """
    # --- Don't recompute colors
    if seen_colors is None:
        seen_colors = {}

    # --- Get the size of the structure
    ysize = len(structure)
    xsize = len(structure[0])
    zsize = len(structure[0][0])

    # --- Convert image to nested list of block names
    blocks = []
    # Bottom up
    for y in range(ysize):
        # Start a slice
        yslice = []
        for x in range(xsize):
            # Add row for each x / row
            yslice.append([])
            # Get each pixel
            for z in range(zsize):
                pixel = structure[y][x]
                if pixel not in seen_colors:
                    block_name = get_block_from_color(pixel)
                    seen_colors[pixel] = block_name
                else:
                    block_name = seen_colors[pixel]
                yslice[-1].append(block_name)
        blocks.append(yslice)
    return blocks, seen_colors
