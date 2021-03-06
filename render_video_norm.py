#!/usr/bin/env python3
import json
import os
from pprint import pprint
import subprocess
import time


def main():

    # Trying to open all_podcasts_w_mp4.json
    if os.path.exists('all_podcasts_w_mp4.json'):
        all_podcasts = 'all_podcasts_w_mp4.json'
    elif os.path.exists('all_podcasts_w_covers.json'):
        all_podcasts = 'all_podcasts_w_covers.json'
    else:
        print('Files all_podcasts_w_mp4.json and all_podcasts_w_covers.json.json do not exist.')
        print('Exit')
        sys.exit(1)

    with open(all_podcasts) as f:
        podcasts = json.load(f)

    for podcast in podcasts:
        print('-' * 100)
        print(podcast['title'])

        if podcast.get('mp4'):
            print('  Video has already been rendered.')
            continue

        mp3 = podcast.get('mp3')
        if not mp3:
            print('  Podcast does not contain mp3 key! Press any key to continue...')
            pprint(podcast)
            input()
            continue

        cover = podcast.get('cover')
        if not cover:
            print('  Podcast does not contain cover key! Press any key to continue...')
            pprint(podcast)
            input()
            continue

        if not os.path.exists(mp3):
            print(f'  File {mp3} does not exist! Press any key to continue...')
            input()
            continue

        if not os.path.exists(cover):
            print(f'  File {cover} does not exist! Press any key to continue...')
            input()
            continue

        mp4 = f'mp4/{mp3.split("/")[1].split(".")[0]}.mp4'
        print(f'  {mp4}')

        cmd = f'ffmpeg -loop 1 -i {cover} -i {mp3} -c:a copy -c:v libx264 -shortest {mp4}'
        run_cmd = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)


        while True:
            if psutil.Process(run_cmd.pid).status() == 'zombie':
                break

        podcast.update({"mp4": mp4})
        with open('all_podcasts_w_mp4.json', 'w') as f:
            json.dump(podcasts, f)

        print('  Finished')

    print('=' * 100)
    print('Changes saved to all_podcasts_w_mp4.json')


if __name__ == '__main__':
    main()
