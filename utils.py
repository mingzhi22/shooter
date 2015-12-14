# -*- coding: utf-8 -*-
import os, math, md5, urllib

def getFileHash(filePath):
    filePath = os.path.expanduser(filePath)
    fileSize = os.path.getsize(filePath)

    if fileSize < 8192:
        print u'文件小于8k, 不是视频文件吧？'
        return

    offsets = (4096, math.floor(fileSize / 3) * 2, math.floor(fileSize / 3), fileSize - 8192)
    bufferSize = 4096
    fd = open(filePath, 'rb')
    md5Arr = []

    for offset in offsets:
        fd.seek(offset)
        buffer = fd.read(bufferSize)

        if len(buffer) < bufferSize:
            print u'读取出错, 内容长度过小'
            return

        m = md5.new()
        m.update(buffer)
        md5Arr.append(m.hexdigest())

    if len(md5Arr) == len(offsets):
        return ';'.join(md5Arr)
    else:
        print u'计算输入文件的md5值出错'
        return

def parseSubtitles(data):
    subtitles = []

    for item in data:
        if not item['Files']:
            continue

        for file in item['Files']:
            if file['Link'] and file['Ext']:
                if file['Ext'] == 'srt' or file['Ext'] == 'ass':
                    subtitles.append({
                        'ext': file['Ext'],
                        'url': file['Link']
                    })

    return subtitles

