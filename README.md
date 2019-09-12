# Deluge Discord Notifications!

This script when configured with deluge, will send you a notification when a torrent is added along with the tracker name.
WHen a torrent is completed, it will send you a message with the name, tracker and RATIO.

Optionally, you can set a second delay, e.g. 60 seconds, and then 60 seconds after torrent completion it will send another message with updated ratio.

## Setup

You must be the owner of a discord server (prefarably set up a private server for this), and [create a discord webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for a channel in it.  You will need the Webhook URL you get for the script.

You need to download the script `dcpush.py` from the repo to your seedbox, you can do it using:

```
wget https://github.com/ckcr4lyf/deluge-dc-notif/raw/master/dcpush.py
```

In this script, you will need to set the Webhook URL you generated, along with a few more things:

|Variable|Explanation|
|--------|-----------|
|delugePort|The port on which deluge DAEMON is running on seedbox|
|delugeUsername|The username for deluge|
|delugePassword|The password for deluge|
|myWebhookURL|The discord webhook URL|
|sendTag|`True` if you want the message to "tag" you on discord, `False` if you want it to just be a message|
|myDiscordID|Your 18 digit discord ID, if you set `sendTag` to `True` in order to tag you|
|ratioCheckDelay|Seconds after completion to send second ratio notification. 0 to disable|
|bot_username|The username from which you'll receive the messages on discord|

Edit the file `dcpush.py` to set these values.

Make the script executable with:

```
chmod +x dcpush.py
```

then, add the whole path to deluge execute plugin, same for both "Torrent Added" and "Torent Complete"

E.g. path: `/some/thing/scripts/dcpush.py`

Restart deluge, and hopefully, next time a torrent is added, it will work!
