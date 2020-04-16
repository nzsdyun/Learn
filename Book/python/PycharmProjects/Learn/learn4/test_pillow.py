# -*- coding: utf-8 -*-
import os
import random

from PIL import Image, ImageFont, ImageDraw, ImageFilter

cur_dir = os.path.abspath('.')
im = Image.open(os.path.join(cur_dir, 'test.png'))
w, h = im.size
print('size:%d,%d, format:%s, mode:%s' % (w, h, im.format, im.mode))
tim = im.thumbnail((w / 2, h / 2))
im.save(os.path.join(cur_dir, 'test_thumbnail.png'), 'png')


def rand_char():
    return chr(random.randint(65, 90))


def ran_bg_rgb():
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)


def ran_tx_rgb():
    return random.randint(32, 255), random.randint(32, 255), random.randint(32, 255)


def create_verification_code():
    width, height = 240, 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font
    font = ImageFont.truetype('arial.ttf', 36)
    # 创建Draw
    draw = ImageDraw.Draw(image)
    # 填充每个像素
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=ran_bg_rgb())
    # 画文字
    for i in range(4):
        draw.text((60 * i + 10, 10), rand_char(), fill=ran_tx_rgb(), font=font)
    # 模糊
    image.filter(ImageFilter.BLUR)
    image.save(os.path.join(cur_dir, 'test_verification_code.png'), 'png')


if __name__ == '__main__':
    create_verification_code()
