#!/usr/bin/env python 

import os
import sys
import urllib2
import json
from threading import Timer

try:
    from delugePushConfig import *
except ImportError:
    print("You do not seem to have a config file. Please download it! Read more: https://github.com/ckcr4lyf/deluge-dc-notif")
    sys.exit(1)

def sendMessage(normalText, title, body, footer=""):

    msg = ""

    if (SEND_TAG == True):
        msg += "<@" + DISCORD_ID + ">, "

    msg += normalText

    values = {
        "content": msg,
        "username": BOT_USERNAME,
        "avatar_url": BOT_AVATAR,
        "embeds": [
            {
                "title": title,
                "description": body,
                "footer": {
                    "text": footer
                }
            }
        ]
    }

    data = json.dumps(values)
    req = urllib2.Request(WEBHOOK_URL, data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Chrome')
    response = urllib2.urlopen(req)

def getSize(lines):
    for line in lines:
        ratioIndex = line.find('Ratio:')
        if (ratioIndex != -1):
            sizeString = line[:ratioIndex - 1]
            return sizeString.split('/')[1]

    return 'Unknown Size'

def getState(torrentHash, torrentName, delayTime=0, delayCall=False):

    delugeCommand = 'deluge-console \"connect 127.0.0.1:' + DELUGE_PORT + ' '  + DELUGE_USERNAME + ' ' + DELUGE_PASSWORD + ' ; info '

    if (DELUGE_VERSION[0] == '2'):
        delugeCommand += '-v '
    
    delugeCommand += torrentHash
    delugeCommand += '\"'
    delugeConsoleResult = os.popen(delugeCommand).read()
    lines = delugeConsoleResult.split('\n')

    if (DELUGE_VERSION[0] == '2'):
        if "Failed to connect to" in lines[0]:
            print(lines[2]) # Prints the error from deluge back to the user
            return
        tracker = lines[7][9:]

        if (lines[2].find('State: Downloading') == 0):
            sendMessage("Added torrent!", torrentName, tracker)
        else:
            ratioIndex = lines[4].find('Share Ratio')
            ratioValue = lines[4][ratioIndex+6:]

            if (delayCall):
                message = 'After {} seconds, ratio update:'.format(str(delayTime))
                sendMessage(message, torrentName, tracker, ratioValue)
            else:
                message = 'Completed torrent!'
                sendMessage(message, torrentName, tracker, ratioValue)

                if (delayTime > 0):
                    delay = Timer(delayTime, getState, (torrentHash, torrentName, delayTime, True))
                    delay.start()

    else:

        torrentSize = getSize(lines)
        trackerIndex1 = delugeConsoleResult.find('\nTracker status:')
        trackerIndex2 = delugeConsoleResult.find(':', trackerIndex1 + 17)
        tracker = delugeConsoleResult[trackerIndex1+17:trackerIndex2]
        torrentNameMessage = torrentName + " ({})".format(torrentSize)

        if (lines[3].find('State: Downloading') == 0):
            sendMessage('Added torrent!', torrentNameMessage, tracker)
        else:
            ratioIndex = lines[5].find('Ratio: ')
            ratioValue = lines[5][ratioIndex:]

            if (delayCall):
                message = 'After {} seconds, ratio update:'.format(str(delayTime))
                sendMessage(message, torrentNameMessage, tracker, ratioValue)
            else:
                message = 'Completed torrent!'
                sendMessage(message, torrentNameMessage, tracker, ratioValue)

                if (delayTime > 0):
                    delay = Timer(delayTime, getState, (torrentHash, torrentName, delayTime, True))
                    delay.start()            

try:
    torrentHash = str(sys.argv[1])
except IndexError:
    print("Missing torrent hash! If you are trying to test, run:\npython delugePush.py [hash]\nWhere [hash] is a hash of a torrent you have in Deluge.")
    sys.exit(1)

torrentName = "Test"

try:
    torrentName = str(sys.argv[2])
except:
    pass

getState(torrentHash, torrentName, RATIO_CHECK_DELAY, False)