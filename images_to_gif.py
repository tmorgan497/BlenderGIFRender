import glob
# from pathlib import Path
# from PIL import Image

import imageio

render_file_path = "/home/tmorg/Downloads/tmp/"
output = "/home/tmorg/Downloads/tmp/output.gif"

# images = []
# for file in glob.glob(render_file_path + "*.png"):
#     file = Path(file)
#     frame = Image.open(file)
#     images.append(frame)

# images[0].save(output,
#                save_all=True,
#                append_images=images[1:],
#                )

images = []
for file in glob.glob(render_file_path + "*.png"):
    images.append(imageio.imread(file))

imageio.mimsave(output, images, fps=24)
