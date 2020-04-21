#!/usr/bin/env python 

import os
import sys
import urllib
import urllib2
import json
from threading import Timer

DELUGE_PORT = "58846" #Replace with the port for deluge daemon (NOT WEBUI) on your seedbox
DELUGE_USERNAME = "deluge" #Replace with your deluge username
DELUGE_PASSWORD = "deluge" #Replace with your deluge password
WEBHOOK_URL = "https://discordapp.com/api/webhooks/somestuff/goeshere" #Replace with your Discord Webhook URL 
SEND_TAG = False #Set to False (capital 'F') if you want it to send a message, but not tag you. Set to True (capital 'T') if you want a tag. Must supply discord ID
DISCORD_ID = "123456789012345678" #ONLY required is senTag is True. Set to your 18 digit Discord ID (NOT YOUR 4 digit code like username#6969) - right click on your username to copy ID.
RATIO_CHECK_DELAY = 60 #Number of seconds after torrent completion to send another ratio update. Set to 0 to disable.
BOT_USERNAME = "TorrentBot" #The username that will appear as the sender fo rnotifications. Set to whatever u want
BOT_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Deluge-Logo.svg/1200px-Deluge-Logo.svg.png" #Avatar of the "bot" in discord. PNG recommened
DELUGE_VERSION = "1.3.15" #Only the first character matches, so 2.0.3 will be same as 2.0.1, and 1.3.15 same as 1.3.0. Make sure first character is 1 (or 2) only.

class not_bot:
    def __init__(self, webhookURL, tag, discordID, botUserName):
        self.webhookURL = webhookURL
        self.tag = tag
        self.discordID = discordID
        self.botUserName = botUserName

    def send_msg(self, tag_msg, title, body, footer=""):

        msg = ""

        if (self.tag == True):
            msg += "<@" + self.discordID + ">, "

        msg += tag_msg

        values = {
            "content": msg,
            "username": self.botUserName,
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
        req = urllib2.Request(self.webhookURL, data)
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'Chrome')
        response = urllib2.urlopen(req)

def query(torrentHash, torrentName, delayTime=0, delayCall=False):

    if (DELUGE_VERSION[0] == "2"):
        cmdString = 'deluge-console \"connect 127.0.0.1:' + DELUGE_PORT + ' '  + DELUGE_USERNAME + ' ' + DELUGE_PASSWORD + ' ; info -v '
        cmdString += torrentHash
        cmdString += '\"'
        myCmd = os.popen(cmdString).read()
        lines = myCmd.split('\n')

        try:
            if (lines[2].index("State: Downloading") == 0):
                #Called because torrent add
                tracker = lines[7][9:]
                myBot.send_msg("Added torrent!", torrentName, tracker)
        
        except:
            # Called because torrent complete, not add.
            tracker = lines[7][9:]
            ratio_index = lines[4].index("Share Ratio")
            ratio_word = lines[4][ratio_index+6:]
            msg = "Completed torrent!"
            if delayCall == True:
                msg = "After " + str(delayTime) + " seconds, ratio update:"
            myBot.send_msg(msg, torrentName, tracker, ratio_word)

            if (delayTime > 0 and delayCall == False):
                # We need to set a delayed call as well.
                delay = Timer(delayTime, query, (torrentHash, torrentName, delayTime, True))
                delay.start()

    else:
        cmdString = 'deluge-console \"connect 127.0.0.1:' + DELUGE_PORT + ' '  + DELUGE_USERNAME + ' ' + DELUGE_PASSWORD + ' ; info '
        cmdString += torrentHash
        cmdString += '\"'
        myCmd = os.popen(cmdString).read()
        lines = myCmd.split('\n')

        try:
            if (lines[3].index("State: Downloading") == 0):
                #Called because torrent add.
                i1 = myCmd.index("\nTracker status:")
                i2 = myCmd.index(":", i1 + 17)

                #Extract the tracker name
                tracker = myCmd[i1 + 17:i2]
                myBot.send_msg("Added torrent!", torrentName, tracker) #We know arg. index 2 is the torrent name.

        except:
            #Called because of torrent complete, not torrent add.
            i1 = myCmd.index("\nTracker status:")
            i2 = myCmd.index(":", i1 + 17)

            tracker = myCmd[i1 + 17:i2]

            #Also want to get the ratio we ended with
            i1 = lines[5].index("Ratio: ")
            ratio_word = lines[5][i1:]

            myBot.send_msg("Completed torrent!", torrentName, tracker, ratio_word)

            if (RATIO_CHECK_DELAY > 0):
                delay = Timer(delayTime, query, (torrentHash, torrentName, delayTime, True))
                delay.start()

myBot = not_bot(WEBHOOK_URL, SEND_TAG, DISCORD_ID, BOT_USERNAME)
torrentHash = str(sys.argv[1])
torrentName = str(sys.argv[2])

query(torrentHash, torrentName, RATIO_CHECK_DELAY, False)