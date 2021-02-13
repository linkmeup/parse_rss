#!/usr/bin/env python3

import requests
import xmltodict
import json
from datetime import datetime


PUBLISH_DATES = {
    "2013": datetime(2021, 2, 28, 12, 00, 3).isoformat() + ".000Z",
    "2014": datetime(2021, 3, 31, 12, 00, 3).isoformat() + ".000Z",
    "2015": datetime(2021, 4, 30, 12, 00, 3).isoformat() + ".000Z",
    "2016": datetime(2021, 5, 31, 12, 00, 3).isoformat() + ".000Z",
    "2017": datetime(2021, 6, 30, 12, 00, 3).isoformat() + ".000Z",
    "2018": datetime(2021, 7, 31, 12, 00, 3).isoformat() + ".000Z",
    "2019": datetime(2021, 8, 31, 12, 00, 3).isoformat() + ".000Z",
    "2020": datetime(2021, 9, 30, 12, 00, 3).isoformat() + ".000Z",
    "2021": datetime(2021, 10, 31, 12, 00, 3).isoformat() + ".000Z",
}


def get_podcasts(rss):
    all_podcasts = []
    for item in rss["channel"]:
        if item  == "item":
            for podcast in rss["channel"][item]:
                short_description = ""
                this_podcast = {}
                
                for head in podcast:
                    if head == "title":
                        this_podcast.update({"title": podcast[head]})

                    elif head == "pubDate":
                        pub_year = podcast[head].split()[3]
                        pub_date = datetime.strptime(podcast[head][5:-6], '%d %b %Y %H:%M:%S').isoformat() + ".000Z"
                        this_podcast.update({"publish_at": PUBLISH_DATES[pub_year]})
                        this_podcast.update({"pub_date": pub_date})
                        print

                all_podcasts.append(this_podcast)

    return all_podcasts


def main():
    print('Start RSS parsing...')
    r = requests.get("https://linkmeup.ru/rss/podcasts")
    rss = xmltodict.parse(r.text)["rss"]

    all_podcasts = get_podcasts(rss)

    with open('all_podcasts_w_mp4.json') as f:
        podcasts = json.load(f)

    for podcast in podcasts:
        for i in all_podcasts:
            if podcast["title"] == i["title"]:
                podcast.update({"recordingDate": i["pub_date"]})
                podcast.update({"publishAt": i["publish_at"]})

    with open('all_podcasts_w_pd.json', 'w') as f:
        json.dump(podcasts, f)

    print('Pub dates are added and dict saved to all_podcasts_w_pd.json.')

if __name__ == '__main__':
    main()
