#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from time import sleep
from pathlib import Path
import requests
import yt_dlp

URL = 'https://www.googleapis.com/youtube/v3'
YTURL = 'https://www.youtube.com'


class YouTube:
    __tries = 3
    __time_sleep = 60

    def __init__(self, key, path, filename):
        self.__key = key
        self.__file = Path(path) / filename

    def get_all(self, channel_id):
        url = f"{URL}/search?channeldId={channel_id}&part=snippet,id&order=date&maxResults=100&key={self.__key}"
        print(url)
        response = requests.get(url=url)
        if response.status_code != 200:
            return None
        data =response.json()
        if 'items' in data and data['items']:
            for item in data['items']:
                print(item)

    def get_info(self, yt_id):
        url = f"{URL}/videos?part=snippet&id={yt_id}&key={self.__key}"
        print(url)
        response = requests.get(url=url)
        if response.status_code != 200:
            return None
        data = response.json()
        if 'items' in data and data['items']:
            item = data['items'][0]
            if item['snippet']['title'].lower() == 'private video' or \
                    item['snippet']['title'].lower() == 'deleted video':
                return None
            link = f"{YTURL}/watch?v={yt_id}"
            return {"title": item['snippet']['title'],
                    "description": item['snippet']['description'],
                    "id": yt_id,
                    "link": link
            }

    def clean(self):
        output = Path(f"{self.__file}.mp4")
        if output.exists():
            os.remove(output)

    def download(self, yt_id):
        self.clean()
        success = False
        ydl_opts = {'outtmpl': f"{self.__file}",
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}
        download_link = f"{YTURL}/watch?v={yt_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            tries = 0
            while tries < self.__tries and success is False:
                try:
                    ydl.download([download_link])
                    success = True
                except Exception as exception:
                    print(exception)
                    tries += 1
                    sleep(self.__time_sleep)
        return success
