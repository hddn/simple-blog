import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


MAX_WIDTH = 600
IMAGE = 'mj.jpg'
TEXT = 'SoftGroupPython'
OPACITY = 0.7

root = os.path.realpath(os.path.dirname(__file__))
path = os.path.join(root, '..', 'static', 'uploads')


def add_watermark(image, text=TEXT, opacity=OPACITY):
    img = Image.open(os.path.join(path, image))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    watermark = Image.new('RGBA', (MAX_WIDTH, img.size[1]), (255, 255, 255, 0))
    waterdraw = ImageDraw.Draw(watermark, 'RGBA')
    water_position = ((MAX_WIDTH - img.size[0]) / 2) + 15
    waterdraw.text((water_position, 15), text)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    watermark.paste(img, ((MAX_WIDTH - img.size[0])/2, 0))
    watermark.save(os.path.join(path, 'w_' + image), 'JPEG')


def edit_image(image, filename):
    img = Image.open(image)
    if img.size[0] > MAX_WIDTH:
        width_prop = (MAX_WIDTH / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(width_prop)))
        img = img.resize((MAX_WIDTH, new_height), Image.ANTIALIAS)
        img.save(os.path.join(path, filename))
        add_watermark(filename)
    else:
        img.save(os.path.join(path, filename))
        add_watermark(filename)


if __name__ == '__main__':
    resize_image()
    image = 'resized_' + IMAGE
    add_watermark(image)
