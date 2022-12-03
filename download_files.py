#!/usr/bin/env python3
import re
import json
import os
import sys
import uuid
import requests

FEEDS  = {
    "LTE": "lte",
    "telecom": "telecom",
    "sysadmins": "sysadmins",
    "По'уехавшие": "emigration",
    "sysadmins_franchise-V0": "sysadmins",
    "Шоты": "shorts",
    "IRL": "irl",
    "Поjncieлки": "poccielki",
    "Поrhcaлки": "poccielki",
    "Поallелки": "poccielki",
    "Поccieлки": "poccielki",
    "По'училки": "poccielki",
    "linkmeup": "other",
}


def get_feed(title):
    first_word = title.split()[0]
    return FEEDS[first_word] if FEEDS.get(first_word) else 'other'


def download_file(url, file_name):
    with open(file_name, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)


def main():

    # Trying to open all_podcasts_w_files.json
    if os.path.exists('all_podcasts_w_files.json'):
        all_podcasts = 'all_podcasts_w_files.json'
    elif os.path.exists('all_podcasts.json'):
        all_podcasts = 'all_podcasts.json'
        print("this one")
    else:
        print('Files all_podcasts_w_files.json and all_podcasts.json do not exist.')
        print('Exit')
        sys.exit(1)

    with open(all_podcasts) as f:
        podcasts = json.load(f)

    for podcast in podcasts:

        print('-' * 100)
        print(podcast['title'])

        # Check if file has already been downloaded
        # In case script was interrupted
        if not podcast.get('mp3'):

            regexp = "https:\/\/dts\.podtrac\.com\/.*\.mp3"
            print(podcast)
            reg_match = re.search(regexp, podcast['description'])
            if reg_match:
                url = reg_match.group()
                podcast.update({'podcast_url': url})
                print(url)
            if not podcast.get('podcast_url'):
                print('  Podcast URL is absent! Press any key to continue...')
                # input()
                continue

            print('  Start downloading mp3...')
            # episode_filenames = uuid.uuid4()
            episode_filenames = podcast['podcast_url'].split("/")[-1]

            download_file(podcast['podcast_url'], f'mp3/{episode_filenames}.mp3')
            podcast.update({'mp3': f'mp3/{episode_filenames}.mp3'})

            print('    Finished.')

            if podcast.get('kdpv'):
                print('  Start downloading img...')
                img = f"img/{episode_filenames}.{podcast['kdpv'].split('.')[-1]}"
                download_file(podcast['kdpv'], img)
                podcast.update({'img': img})
                print('    Finished.')
            else:
                print('  No KDPV. Using default...')
                podcast.update({'img': f"img/defaults/{get_feed(podcast['title'])}_img.png"})
                print('    Finished.')

            podcast.update({'feed': get_feed(podcast['title'])})

            with open('all_podcasts_w_files.json', 'w') as f:
                json.dump(podcasts, f)
        else:
            print('  mp3 has already been downloaded')

    print('=' * 100)
    print('Changes saved to all_podcasts_w_files.json')


if __name__ == '__main__':
    main()
