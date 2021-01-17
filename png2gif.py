import glob
import os
from PIL import Image
import ffmpeg

def gifWriter():
    # filepaths
    fp_in = "./maze*.png"
    fp_out = "./movie.gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=800, loop=0)
    for file in glob.glob("maze*.png"):
        os.remove(file)

def movieWriter():
    (
        ffmpeg
        .input('./maze*.png', pattern_type='glob', framerate=25)
        .output('movie.mp4')
        .run()
    )
    for file in glob.glob("maze*.png"):
        os.remove(file)