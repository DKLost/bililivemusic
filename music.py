#!/usr/bin/python
import json
import re
import time
import os
import pyglet
import requests

pgmusic = pyglet.media
url = 'https://api.live.bilibili.com/ajax/msg'
form = {
    'roomid': 5103982,
    'csrf_token': '6f10a58cd00bc03cf89405b811212c6a'
}
timeline = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
tos = open('music/text_on_screen.txt', 'w+')
player = pgmusic.Player()


def Search(keywords, stype=1, offset=0, total='true', limit=1):
    url = 'http://music.163.com/api/search/get/web?csrf_token='
    params = dict(
        s=keywords,
        type=stype,
        offset=offset,
        total=total,
        limit=limit
    )
    content = requests.post(url, params).content
    html = json.loads(content)
    try:
        song = html['result']['songs'][0]
    except:
        return
    else:
        return song


def Download(sid, path):
    url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(sid)
    with open(path, "wb+") as nf:
        nf.write(requests.get(url).content)


def addsong(song):
    path = "music/{}-{}.mp3".format(
        song['name'], song['artists'][0]['name'])
    path = path.encode('utf-8')
    if not os.path.exists(path):
        try:
            Download(song['id'], path)
        except:
            return
    player.queue(pgmusic.load(path))


def newdm(dmt):
    global timeline
    for x in dmt:
        if x['timeline'] > timeline:
            dmtest(x['text'])
            timeline = x['timeline']


def dmtest(text):
    if re.match('^点歌 ', text):
        song = Search(text[3:len(text)])
        if song:
            addsong(song)
    elif re.match('^切歌$', text):
        player.next_source()


while True:
    html = requests.post(url, form)
    jsondata = html.content.decode('unicode_escape')
    try:
        dmt = (json.loads(jsondata))['data']['room']
    except:
        pass
    else:
        newdm(dmt)
    if not player.playing:
        player.play()
    time.sleep(1)


#text = json.dumps(dm, ensure_ascii=False, indent=1)
