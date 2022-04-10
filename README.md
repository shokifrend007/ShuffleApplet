# ShuffleApplet

A small python programm that creates an icon on the taskbar, allowing you to shuffle a folder of music.

## Setup

Run this command to install needed packages:

```
sudo apt install ffmpeg python3 python3-pip libasound2-dev libxcb-xinerama0
```

Run this command to install needed python packages:

```
pip3 install pyside2 simpleaudio pydub
```

Make `main.py` executable:

```
chmod u+x main.py
```

(optional) Move the `ShuffleApplet` folder into `/opt`:

```
sudo mv ShuffleApplet /opt/
```

Test it!

```
/path/to/ShuffleApplet/main.py
```

Now you can add this to your startup applications:

```
bash -c "cd /path/to/ShuffleApplet; ./main.py; exit"
```

## Config

Look at the comments in `config.json` for more info.

## Pro tip

Set up multiple instances for different playlist/folder and add them all to the startup applications.

## License

This project is under the GNU GPLv2 license.

The example music used is by HoliznaCC0 from https://freemusicarchive.org/music/holiznacc0/lost under the CC0 license.
