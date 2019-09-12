#!/usr/bin/env python 

import os
import sys
import urllib
import urllib2
import json
from threading import Timer

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

def afterTime(cmdstr, thebot, rcd):
    myCmd = os.popen(cmdstr).read()
    lines = myCmd.split('\n')

    #Called because of torrent complete, not torrent add.
    i1 = myCmd.index("\nTracker status:")
    i2 = myCmd.index(":", i1 + 17)

    tracker = myCmd[i1 + 17:i2]

    #Also want to get the ratio we ended with
    i1 = lines[5].index("Ratio: ")
    ratio_word = lines[5][i1:]

    msg = "After " + str(rcd) + " seconds, ratio update:"

    thebot.send_msg(msg, sys.argv[2], tracker, ratio_word)

delugePort = "58846" #Replace with the port for deluge daemon (not WEBUI) on your seedbox
delugeUsername = "deluge" #Replace with your deluge username
delugePassword = "deluge" #Replace with your deluge password
myWebhookURL = "https://discordapp.com/api/webhooks/some/stuff" #Replace with your Discord Webhook URL 
sendTag = True #Set to False (capital 'F') if you want it to send a message, but not tag you.
myDiscordID = "123456789012345678" #Set to your 18 digit Discord ID (NOT YOUR 4 digit code like username#6969) - right click on your username to copy ID.
ratioCheckDelay = 60 #Number of seconds after torrent completion to send another ratio update. Set to 0 to disable.
bot_username = "TorrentBot" #The username that will appear as the sender fo rnotifications. Set to whatever u want

myBot = not_bot(myWebhookURL, sendTag, myDiscordID, bot_username)

cmdString = 'deluge-console \"connect 127.0.0.1:' + delugePort + ' '  + delugeUsername + ' ' + delugePassword + ' ; info '
cmdString += str(sys.argv[1])
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
        myBot.send_msg("Added torrent!", sys.argv[2], tracker) #We know arg. index 2 is the torrent name.

except:
    #Called because of torrent complete, not torrent add.
    i1 = myCmd.index("\nTracker status:")
    i2 = myCmd.index(":", i1 + 17)

    tracker = myCmd[i1 + 17:i2]

    #Also want to get the ratio we ended with
    i1 = lines[5].index("Ratio: ")
    ratio_word = lines[5][i1:]

    myBot.send_msg("Completed torrent!", sys.argv[2], tracker, ratio_word)

    if (ratioCheckDelay > 0):
        delay = Timer(ratioCheckDelay, afterTime, (cmdString, myBot, ratioCheckDelay))
        delay.start()