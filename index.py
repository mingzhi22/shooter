#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, urllib, json
from utils import *

reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv) < 2:
    print u'使用方法: python index.py 视频文件路径'
    exit(22)

filePath = os.path.abspath(sys.argv[1])

if not os.path.isfile(filePath):
    print u'视频不存在: ' + filePath
    exit(2)

hash = getFileHash(filePath)

if not hash:
    print u'计算视频Hash出错'
    exit(1)

data = urllib.urlencode({
        'filehash': hash,
        'pathinfo': filePath,
        'format': 'json',
        'lang': 'Chn'
    })

u = urllib.urlopen('http://www.shooter.cn/api/subapi.php', data)

try:
    subtitles = parseSubtitles(json.loads(u.read()))
except Exception as e:
    subtitles = ''

if subtitles and len(subtitles):
    extCount = {}

    for subtitle in subtitles:
        ext = subtitle['ext']

        if ext in extCount:
            extCount[ext] += 1
        else:
            extCount[ext] = 0

        pathInfo = os.path.splitext(filePath)

        subtitlePath = (pathInfo[0] + ('.' + str(extCount[ext]) if extCount[ext] else '') + '.chi.' + ext).encode('utf-8')
        if not os.path.isfile(subtitlePath):
            print u'下载字幕: ' + subtitlePath
            urllib.urlretrieve(subtitle['url'], subtitlePath)
        else:
            print u'字幕存在: ' + subtitlePath
else:
    print u'暂无字幕: ' + filePath
