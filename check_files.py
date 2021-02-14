#!/usr/bin/env python3
import json
import os
import sys


def check_files(podcasts, item):

    total_size = 0
    for podcast in podcasts[::-1]:
        print('-' * 100)
        print(podcast['title'])

        if podcast.get(item):
            print(f'  {podcast.get(item)}')
            file_name = podcast.get(item)
            try:
                file_size = os.path.getsize(file_name)
                total_size += file_size
                print(f'  {file_name} - {file_size}')

                if file_size == 0:
                    print(f'  ACHTUNG!!! File size is ZERO!')
                    input()
            except FileNotFoundError as e:
                print('  ACHTUNG!!!', e)
                input()
        else:
            print(f'  No Way! Key {item} not found')
            input()

    return total_size


ITEMS = [
    'img',
    'cover',
    'mp3',
    'mp4'
]


def main():
    file = sys.argv[1]
    item = sys.argv[2]
    try: 
        with open(file) as f:
            podcasts = json.load(f)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    if not item in ITEMS:
        print(f"Can't check unexisting item {item}")
        sys.exit(1)

    total_size = check_files(podcasts, item)

    print('=' * 100)
    print(f'{item}. Total size: {round(total_size / 1024**2, 2)} MB')


if __name__ == '__main__':
    main()
