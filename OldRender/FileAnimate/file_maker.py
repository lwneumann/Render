import cv2, os
from PIL import Image
from datetime import datetime
from alive_progress import alive_bar


def clear_output():
    for file_name in os.listdir('output/'):
        file_path = os.path.join('output/', file_name)
        if os.path.isfile(file_path) and file_name.endswith(".png"):
            os.remove(file_path)
    return


def array_to_png(array, filename="test", folder="output", mode="RGB"):
    """
    Modes:
        - RGB
        - RGBA
        - L (8 bit greyscale)
    """
    height = len(array)
    width = len(array[0]) if height > 0 else 0

    # Flatten
    pixels = [pixel for row in array for pixel in row]

    img = Image.new(mode, (width, height))
    img.putdata(pixels)

    path = f"./{folder}/{filename}.png"
    img.save(path)
    return


def make_mp4(name=None, folder="output", vid_folder=".", fps=30):
    if name is None:
        name = "test" + datetime.now().strftime("%y%m%d-%H%M%S")

    image_files = sorted(
        [f for f in os.listdir(folder+"/") if f.endswith(".png")],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    first_image_path = os.path.join(folder+'/', image_files[0])
    frame = cv2.imread(first_image_path)
    h, w, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for MP4 format
    video = cv2.VideoWriter(vid_folder+"/"+name+'.mp4', fourcc, fps, (w, h))

    print(f"{f'-Saving as {vid_folder}/{name}.mp4': <79}|")

    with alive_bar(len(image_files)) as rbar:
        for image_name in image_files:
            image_path = os.path.join(folder+"/", image_name)
            frame = cv2.imread(image_path)
            video.write(frame)
            rbar()

    video.release()
    print('|' + ' '*78 + '|')
    print(f'{"-Cleared Images": <79}|')
    clear_output()

    return


def render_video(step, frames=90, fps=30, mode="RGB", video_folder="."):
    print()
    print(f'[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):-<76}-]')
    print('|' + ' '*78 + '|')
    print(f'{f"-Rendering {frames} frames": <79}|')

    last_frame = None

    with alive_bar(frames) as bar:
        for i in range(frames):
            last_frame = step(i, last_frame)
            array_to_png(last_frame, i, mode=mode)
            bar()

    print('|' + ' '*78 + '|')
    make_mp4(fps=fps, vid_folder=video_folder)
    print('|' + ' '*78 + '|')
    print(f'[-{datetime.now().strftime("%y/%m/%d-%H:%M:%S"):->76}-]')
    print()
    print()
    return


if __name__ == "__main__":
    print('hi :3')
    clear_output()
    print('cleared output folder')
