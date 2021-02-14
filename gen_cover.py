#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import os
import sys
import json

FONT = 'Lato-Bold.ttf'

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def prepare_text(text):
    words = text.replace('_', ' ').split()
    if len(text) < 50:
        letters = 17
    elif len(text) < 80:
        letters = 21
    else:
        letters = 26
    text = ''
    row = ''
    for word in words:
        if len(row+word)+1 <= letters: 
            row += f'{word} '
            text += f'{word} '
        else:
            row += f'\n{word} '
            text += f'\n{word} '
            row = word

    return text


def add_text(img, text):
    draw = ImageDraw.Draw(img)
    if len(text) < 50:
        font_size = 70
    elif len(text) < 80:
        font_size = 60
    else:
        font_size = 40
    font = ImageFont.truetype(FONT, font_size)
    draw.text((585, 224), prepare_text(text), (0, 0, 0), font=font)


def prepare_img(img):
    width, height = img.size
    if width <= height:
        width_new = 480
        height_new = int(480/width*height)
    else: 
        height_new = 550
        width_new = int(550/height*width)

    img = img.resize((width_new, height_new), Image.ANTIALIAS)
    img = img.crop((0, 0, 480, 550))
    img = add_corners(img, 20)

    return img


def main():

    # Trying to open all_podcasts_w_files.json
    if os.path.exists('all_podcasts_w_covers.json'):
        all_podcasts = 'all_podcasts_w_covers.json'
    elif os.path.exists('all_podcasts_w_files.json'):
        all_podcasts = 'all_podcasts_w_files.json'
    else:
        print('Files all_podcasts_w_covers.json and all_podcasts_w_files.json do not exist.')
        print('Exit')
        sys.exit(1)

    with open(all_podcasts) as f:
        podcasts = json.load(f)

    for podcast in podcasts[::-1]:
        print('-' * 100)
        print(podcast['title'])
        if podcast.get('cover'):
            print('  Cover has already been generated')
            continue

        cover = Image.open(f'img/defaults/{podcast["feed"]}.jpg')
        if podcast.get('img') and os.path.exists(podcast.get('img')):
            try:
                img = prepare_img(Image.open(podcast['img'])).convert('RGBA')
            except UnidentifiedImageError as e:
                print(f"  Can't open image {podcast['img']}. Continue with default")
                input()
                img = prepare_img(Image.open(f'img/defaults/{podcast["feed"]}_img.png')).convert('RGBA')
        else:
            img = prepare_img(Image.open(f'img/defaults/{podcast["feed"]}_img.png')).convert('RGBA')

        r, g, b, m = img.split()
        top = Image.merge("RGB", (r, g, b))
        mask = Image.merge("L", (m,))
        cover.paste(top, (44,83), mask)

        add_text(cover, podcast['title'])

        img_name = f'img/covers/{podcast.get("mp3").split("/")[1].split(".")[0]}.png'
        cover.save(img_name)
        
        podcast['cover'] = img_name

        with open('all_podcasts_w_covers.json', 'w') as f:
            json.dump(podcasts, f)

    print('=' * 100)
    print('Finished')


if __name__ == '__main__':
    main()

