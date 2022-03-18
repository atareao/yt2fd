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
from pathlib import Path
from time import sleep
from vault import YTIDS
from ytapi import YouTube
from fdapi import PeerTube

def main():
    print("== Init ==")
    yt_key = os.getenv("YT_KEY")
    pt_channel_id = os.getenv("PT_CHANNEL_ID")
    pt_path = os.getenv("PT_PATH")
    filename = os.getenv("VAULT_PATH")
    temp_path = os.getenv("TEMP_PATH")
    temp_filename = os.getenv("TEMP_FILENAME")
    if yt_key is None:
        print(f"{yt_key} not exists")
        exit(1)
    if filename is None or not Path(filename).exists() or \
            not Path(filename).is_file():
        print(f"{filename} not exists")
        exit(1)
    if temp_path is None or not Path(temp_path).exists() or \
            not Path(temp_path).is_dir():
        print(f"{temp_path} not exits")
        exit(1)
    if temp_filename is None:
        print(f"{temp_filename} not exits")
        exit(1)
    youtube = YouTube(yt_key, temp_path, temp_filename)
    peertube = PeerTube(pt_path)

    ytids = YTIDS(filename)
    ytid = ytids.get_id()
    while ytid:
        info = youtube.get_info(ytid)
        print("Downloading:")
        print(info)
        if info and youtube.download(ytid):
            filepath = Path(temp_path) / f"{temp_filename}.mp4"
            contador = 0
            while not filepath.exists() and contador < 10:
                sleep(60)
                print(f"Waiting for {filepath} in {contador} times")
                contador += 1
            if not filepath.exists():
                print(f"{filepath} not exits. Exit")
                exit(1)
            if peertube.upload(pt_channel_id, filepath, info['title'],
                    info['description']):
                ytids.save()
            youtube.clean()
            sleep(60)
        else:
            print(f"Can not download {ytid}")
            exit(1)
        ytid = ytids.get_id()

if __name__ == "__main__":
    main()
