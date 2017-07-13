#!/usr/bin/env python3
import sys
import search
import download
import player
import speech
from PyQt5 import QtWidgets
from gui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.current_video_id = str()

        self.music_player = player.Player()

        self.horizontalSlider.setValue(100)
        self.horizontalSlider.valueChanged.connect(self.update_volume)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_mute.clicked.connect(self.media_mute)
        self.pushButton_play.clicked.connect(self.media_play)
        self.pushButton_pause.clicked.connect(self.media_pause)
        self.pushButton_stop.clicked.connect(self.media_stop)
        self.pushButton_search.clicked.connect(self.start_text)
        self.pushButton_voice.clicked.connect(self.start_voice)

    def search_and_download(self, search_terms):
        self.current_video_id = search.search(search_terms)
        download.download(self.current_video_id)

    def start_text(self):
        self.search_and_download(self.lineEdit.text())
        self.media_open(self.current_video_id + '.flac')
        self.media_play()

    def start_voice(self):
        self.search_and_download(speech.transcribe())
        self.media_open(self.current_video_id + '.flac')
        self.media_play()

    def update_volume(self):
        volume = self.horizontalSlider.value() + 1
        self.music_player.set_volume(volume)
        self.label_volume.setText(str(volume) + '%')

    def media_mute(self):
        self.music_player.mute()
        self.pushButton_mute.setText('Unmute')
        self.pushButton_mute.clicked.disconnect()
        self.pushButton_mute.clicked.connect(self.media_unmute)

    def media_unmute(self):
        self.music_player.unmute()
        self.pushButton_mute.setText('Mute')
        self.pushButton_mute.clicked.disconnect()
        self.pushButton_mute.clicked.connect(self.media_mute)

    def media_play(self):
        self.music_player.play()
        self.label_status.setText('Playing')

    def media_pause(self):
        self.music_player.pause()
        self.label_status.setText('Paused')

    def media_stop(self):
        self.music_player.stop()
        self.label_status.setText('Stopped')

    def media_open(self, file):
        self.music_player.open(file)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
