# Deluge Discord Notifications

This script when configured with Deluge, will send you a notification when a torrent is added along with the tracker name.
When a torrent is completed, it will send you a message with the name, tracker, ratio & size.

Optionally, you can set a second delay, e.g. 60 seconds, and then 60 seconds after torrent completion it will send another message with updated ratio.

## Thanks

<center>

[<img src="https://user-images.githubusercontent.com/6680615/88460516-56eac500-cecf-11ea-8552-584eaaac5297.png" width="300">](https://clients.walkerservers.com/)

Massive Thanks to <a href="https://clients.walkerservers.com/">WalkerServers</a> for sponsoring this project. Check them out for affordable & performant dedicated servers!
</center>


## Setup

You must be the owner of a discord server (prefarably set up a private server for this), and [create a discord webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for a channel in it.  You will need the Webhook URL you get for the script.

You need to clone this repository and go into it next, for which you can run:

```sh
git clone https://github.com/ckcr4lyf/deluge-dc-notif.git
cd deluge-dc-notif
```

Next, we need to configure certain variables in `delugePushConfig.py`. The explanation for the variables is as follows:

|Variable|Explanation|
|--------|-----------|
|DELUGE_PORT|The port on which deluge DAEMON is running on seedbox|
|DELUGE_USERNAME|The username for deluge daemon|
|DELUGE_PASSWORD|The password for deluge daemon|
|WEBHOOK_URL|The discord webhook URL|
|SEND_TAG|`True` if you want the message to "tag" you on discord, `False` if you want it to just be a message|
|DISCORD_ID|Your 18 digit discord ID, if you set `SEND_TAG` to `True` in order to tag you|
|RATIO_CHECK_DELAY|Seconds after completion to send second ratio notification. 0 to disable|
|BOT_USERNAME|The username from which you'll receive the messages on discord (Optional: leave as `""` to use the webhook default)|
|BOT_AVATAR|The avatar (image URL) of the bot which sends the message. PNG advised (Optional: leave as `""` to use the webhook default)|
|DELUGE_VERSION|Your deluge version. Default `1.3.15`, only the first character counts. So `2.0.1` and `2.0.3` have same effect|

Open `delugePushConfig.py` in whatever editor you prefer to make the changes, and then save.

### Python Version

On your machine, run:
```
python -V
```

to determine which version of python you're on, and accordingly which script to use.

* For Python 2.x, use `delugePush.py`
* For Python 3.x, use `delugePush3.py`

The instructions below use `delugePush.py`, please adjust it if required

### Adding to Deluge


Next, make the main script executable by running:

```
chmod +x delugePush.py
```

Then, add the whole path to deluge execute plugin. If you do not know the complete path, you can run
```sh
echo "$PWD/delugePush.py"
```
in your terminal to get it.

It should look something like
```
/home/username/scripts/deluge-dc-notif/delugePush.py
```
Add this for both `Torrent Added` & `Torrent Completed` in Deluge.

Restart deluge, and hopefully, next time a torrent is added, it will work!

## Testing

You can manually test the script by running
```sh
python delugePush.py [infohash]
```
Where `[infohash]` is a 40-character torrent hash. The torrent must exist in Deluge. If all goes well, you should get a notification!

## Docker Setup

If you run deluge in docker, then there may be a permission issue accessing the deluge config folder. 

One naive solution is to `chmod -R 0777 /root` in the deluge container. If you are more concerned around permissions, you can try and make it tighter. If you find a more approrpriate fix please let me know!

For more info, check out [this](https://github.com/ckcr4lyf/deluge-dc-notif/issues/6#issuecomment-1325211650) and [this](https://github.com/ckcr4lyf/deluge-dc-notif/issues/10#issuecomment-1383052525).