#! /usr/bin/python3

import os
import random
import sys
import json

from PySide2 import QtWidgets, QtGui

import simpleaudio
import pydub

from time import sleep

import threading
import subprocess

with open("config.json") as f:
    config = json.load(f)


class Main(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon("logo.png"))
        self.setToolTip(config["tooltip"])
        menu = QtWidgets.QMenu(parent)

        self.startstop_action = menu.addAction("Start")
        self.startstop_action.triggered.connect(lambda: self.startstop())
        self.skip_action = menu.addAction("Skip")
        self.skip_action.triggered.connect(lambda: self.playjob.stop())
        self.activesong = menu.addAction("No song playing")
        self.activesong.triggered.connect(lambda: self.open_song())

        menu.addSeparator()

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: self.exit())

        self.setContextMenu(menu)

        self.is_active = False

        self.tracks = os.listdir(config["musicFolder"])

        self.playjob = simpleaudio.play_buffer(b"", 2, 2, 44100)

        if config["start"]:
            self.startstop()

    def open_song(self):
        if self.activesong.text() != "No song playing":
            subprocess.Popen([config["open"],
                             os.path.join(config["musicFolder"],
                             self.activesong.text())])

    def startstop(self):
        if self.is_active:
            self.startstop_action.setText("Start")
            self.setIcon(QtGui.QIcon("logo.png"))
            self.is_active = False
            self.playjob.stop()
            self.activesong.setText("No song playing")
        else:
            self.startstop_action.setText("Stop")
            self.setIcon(QtGui.QIcon("logo-active.png"))
            self.is_active = True
            self.playthread = threading.Thread(target=self.start)
            self.playthread.start()

    def start(self):
        while self.is_active:
            track = random.choice(self.tracks)
            self.activesong.setText(track)
            segment = pydub.AudioSegment.from_file(
                                    os.path.join(config["musicFolder"], track))
            segment = segment + config["volume"]
            self.playjob = simpleaudio.play_buffer(segment.raw_data,
                                                   segment.channels,
                                                   segment.sample_width,
                                                   segment.frame_rate)
            while self.playjob.is_playing():
                sleep(config["checkInterval"])

    def skip(self):
        self.playjob.stop()

    def exit(self):
        self.is_active = False
        self.playjob.stop()
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = Main(w)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
