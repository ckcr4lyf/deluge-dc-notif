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
IMPORTANT: If you are "updating" the script, perhaps save a backup of the old one, you will need to set the variables again.

In this script, you will need to set the Webhook URL you generated, along with a few more things:

|Variable|Explanation|
|--------|-----------|
|DELUGE_PORT|The port on which deluge DAEMON is running on seedbox|
|DELUGE_USERNAME|The username for deluge daemon|
|DELUGE_PASSWORD|The password for deluge daemon|
|WEBHOOK_URL|The discord webhook URL|
|SEND_TAG|`True` if you want the message to "tag" you on discord, `False` if you want it to just be a message|
|DISCORD_ID|Your 18 digit discord ID, if you set `SEND_TAG` to `True` in order to tag you|
|RATIO_CHECK_DELAY|Seconds after completion to send second ratio notification. 0 to disable|
|BOT_USERNAME|The username from which you'll receive the messages on discord|
|BOT_AVATAR|The avatar (image URL) of the bot which sends the message. PNG advised|
|DELUGE_VERSION|Your deluge version. Default `1.3.15`, only the first character counts. So `2.0.1` and `2.0.3` have same effect|

Edit the file `dcpush.py` to set these values.

Make the script executable with:

```
chmod +x dcpush.py
```

then, add the whole path to deluge execute plugin, same for both "Torrent Added" and "Torent Complete"

E.g. path: `/some/thing/scripts/dcpush.py`

Restart deluge, and hopefully, next time a torrent is added, it will work!
