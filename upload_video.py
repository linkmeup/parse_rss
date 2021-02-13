#!/usr/bin/env python3
import json
import copy
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google_auth_oauthlib.flow


CLIENT_SECRETS_FILE = 'client_secrets.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

UPLOAD_BODY_TEMPLATE = {
    'snippet': {
        'categoryId': 28,
        'title': '',
        'description': '',
        'tags': ['linkmeup', 'networking', 'technology', 'podcast', 'подкасты'],
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': None,
        'selfDeclaredadeForKids': False,
    },
    'recordingDetails': {
        'recordingDate': None
    }
}

PLAYLIST_BODY_TEMPLATE =  {
    'snippet': {
        'playlistId': '',
        'position': 0,
        'resourceId': {
            'kind': 'youtube#video',
            'videoId': ''
        }
    }
}

PLAYLIS_IDS = {
    'telecom': 'PLHN9m7XN8U8HPjkJ-0PpZ493xNvQoFyFc',
    'sysadmins': 'PLHN9m7XN8U8HM90YNcLRc8-_MBI4lCsSO',
    'lte': 'PLHN9m7XN8U8HUvXi0bB6lGTJ5K8yOPR6q',
    'poccielki': 'PLHN9m7XN8U8H22Xpmd-sMjTiS0woNLKaA',
    'emigration': 'PLHN9m7XN8U8EqpFFiQoFJ9NVJvi2VU7Hj',
    'irl': 'PLHN9m7XN8U8EKXAoSlpbgmdjbOYd78BM0',
    'shorts': 'PLHN9m7XN8U8EfgSMi9Es6TuLCLJgjL9g5',
    'other': 'PLHN9m7XN8U8G2bDGE66-JVsV3fezZnZtC'
}


def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def main():
    service = get_authenticated_service()

    with open('all_podcasts_w_pd.json') as f:
        podcasts = json.load(f)


    for podcast in podcasts[::-1]:
        print('='*100)
        print(podcast['title'])

        if podcast.get('youtube_id'):
            print('  Video has already been uploaded.')
            continue

        mp4 = podcast.get('mp4')
        if not mp4:
            print("  OH, MY! No MP4!")
            input()
            continue

        media_file = MediaFileUpload(mp4)

        upload_body = copy.deepcopy(UPLOAD_BODY_TEMPLATE)
        upload_body['snippet']['title'] = podcast['title']
        upload_body['snippet']['description'] = podcast['body']
        upload_body['snippet']['tags'].append(podcast['category'])

        upload_body['status']['publishAt'] = podcast['publishAt']

        upload_body['recordingDetails']['recordingDate'] = podcast['recordingDate']

        response_upload = service.videos().insert(
            part='snippet,status,recordingDetails',
            body = upload_body,
            media_body = media_file
            ).execute()

        print(f'  Video is uploaded: https://www.youtube.com/watch?v={response_upload["id"]}')

        podcast.update({"youtube_id": response_upload["id"]})
        with open('all_podcasts_w_ytid.json', 'w') as f:
            json.dump(podcasts, f)

        print('  all_podcasts_w_ytid.json updated')

        if podcast['category'] in PLAYLIS_IDS:
            playlist_id = PLAYLIS_IDS[podcast['category']]
        else:
            playlist_id = PLAYLIS_IDS['other']

        playlist_body = copy.deepcopy(PLAYLIST_BODY_TEMPLATE)
        playlist_body['snippet']['playlistId'] = playlist_id
        playlist_body['snippet']['resourceId']['videoId'] = response_upload['id']

        request = service.playlistItems().insert(part='snippet', body=playlist_body).execute()

        print('  Added to playlist')
        input()


if __name__ == '__main__':
    main()
