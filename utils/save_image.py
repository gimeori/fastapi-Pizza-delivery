import datetime
import os
from PIL import Image, ImageFile

def image_add_origin(image, folder):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S-%f")
    image = Image.open(image.file)
    path_image = os.path.join(folder, f'{formatted_time}.webp')
    image.save(path_image, format='Webp', quality=100, optimize=True)
    return path_image
