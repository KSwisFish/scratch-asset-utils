# from StringIO import StringIO
import getopt
import gzip
import json
import sys
import os
import requests
import urllib
import re

pretend = False
downloaded = set()
cdn = 'http://cdn.assets.scratch.mit.edu'

def download_file(url, path):
    if os.path.exists(path):
        print("skip:" + path)
        return
    floder = "/".join(path.split("/")[0:-1])
    if not os.path.exists(floder):
        os.makedirs(floder)
    res = requests.get(url)
    if path in downloaded:
        return None
    if res.status_code == 200:
        print(path)
        with open(path, "wb") as f:
            f.write(res.content)
            downloaded.add(path)
            return res.content
    else:
        return None


def download_media(json_path):
    if not json_path: return None
    media_url = "https://cdn.assets.scratch.mit.edu/internalapi/asset/%s/get/"
    thumbnails_url = "https://cdn.scratch.mit.edu/scratchr2/static/__628c3a81fae8e782363c36921a30b614__/medialibrarythumbnails/8d508770c1991fe05959c9b3b5167036.gif"
    download_path = "scratch3/internalapi/asset/"
    json_name = json_path.split("/")[-1]


    with open(json_path, "r",encoding="utf8") as f:
        media = json.load(f)
        for m in media:
            res = download_file(media_url % m['md5'], download_path + m['md5'])
            if json_name == "sprites.json":
                # download sprite
                with open(download_path + m['md5'], "r") as s:
                    sprite = json.load(s)
                    for sound in sprite.get('sounds', []):
                        download_file(media_url % sound['md5'], download_path + sound['md5'])
                    for costume in sprite.get('costumes', []):
                        download_file(media_url % costume['baseLayerMD5'], download_path + costume['baseLayerMD5'])


# download_media("scratch3/json_index/backdrops.json")
download_media("scratch3/json_index/costumes.json")
# download_media("scratch3/json_index/sounds.json")