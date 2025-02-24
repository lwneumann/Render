from PIL import Image
import os


def average_color(img_path):
    # Open the image
    img = Image.open(img_path)

    # Get the image data
    img = img.convert("RGB")
    data = img.getdata()

    # Calculate the average color
    avg_color = (
        sum(pixel[0] for pixel in data) // len(data),
        sum(pixel[1] for pixel in data) // len(data),
        sum(pixel[2] for pixel in data) // len(data)
    )

    return avg_color


def get_block_colors():
    block_folder_path = "./block/"
    files = [f for f in os.listdir(block_folder_path) if os.path.isfile(os.path.join(block_folder_path, f))]
    blocks = []
    for b in files:
        # Block Name without .png, average color
        blocks.append((b[:-4], average_color(block_folder_path+b)))
    return blocks
