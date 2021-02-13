#!/usr/bin/env python3
import json
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
    with open('all_podcasts.json') as f:
        podcasts = json.load(f)

    for podcast in podcasts:

        print('-' * 100)
        print(podcast['title'])

        # Check if file has already been downloaded
        # In case script was interrupted
        if not podcast.get('mp3'):
            if not podcast.get('podcast_url'):
                print('  Podcast URL is absent! Press any key to continue...')
                input()
                continue

            print('  Start downloading mp3...')
            episode_filenames = uuid.uuid4()

            # download_file(podcast['podcast_url'], f'mp3/{episode_filenames}.mp3')
            podcast.update({'mp3': f'mp3/{episode_filenames}.mp3'})

            print('    Finished.')

            if podcast.get('kdpv'):
                print('  Start downloading img...')
                img = f"img/{episode_filenames}.{podcast['kdpv'].split('.')[-1]}"
                # download_file(podcast['kdpv'], img)
                podcast.update({'img': img})
                print('    Finished.')
            else:
                print('  No KDPV. Using default...')
                podcast.update({'img': f"img/defaults/{get_feed(podcast['title'])}_img.png"})
                print('    Finished.')

            with open('all_podcasts_w_files.json', 'w') as f:
                json.dump(podcasts, f)

    print('=' * 100)
    print('Saved to all_podcasts_w_files.json')


if __name__ == '__main__':
    main()
