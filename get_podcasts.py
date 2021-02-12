#!/usr/bin/env python3
import re
import requests
import xmltodict
import json
from html.parser import HTMLParser
from datetime import datetime

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data


def get_podcast_kdpv(description):
    regexp = '<img src="(?P<img>.*?)"'
    match = re.search(regexp, description)

    if match:
        if not "patreon" in match.group("img"):
            return match.group("img")


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
                    elif head == "link":
                        link = podcast[head]
                        this_podcast.update({"link": link})
                    elif head == "enclosure":
                        for thing in podcast[head]:
                            if thing == "@url":
                                this_podcast.update({"podcast_url": podcast[head][thing]})
                    elif head == "itunes:summary":
                        short_description = podcast[head]
                    elif head == "description":
                        img = get_podcast_kdpv(podcast[head])
                        if img:
                            this_podcast.update({"kdpv": img})
                        description = podcast[head]

                if len(short_description) > 20:
                    body = f"{short_description}\n\n{link}"
                else:
                    f = HTMLFilter()
                    f.feed(description)
                    
                    body = f"{f.text}\n\n{link}"

                this_podcast.update({"body": body})

                all_podcasts.append(this_podcast)

    return all_podcasts


def main():
    r = requests.get("https://linkmeup.ru/rss/podcasts", verify=False)
    rss = xmltodict.parse(r.text)["rss"]

    all_podcasts = get_podcasts(rss)

    with open('all_podcasts.json', 'w') as f:
        json.dump(all_podcasts, f)


if __name__ == '__main__':
    main()
