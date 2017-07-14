#!/usr/bin/env python3
import sys
import os
import search
import download
import player
import speech
from PyQt5 import QtWidgets
from gui import Ui_MainWindow
try:
    import sense_hat
    import icons
except ModuleNotFoundError:
    print('Couldn\'t import sense_hat')


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.ext = '.flac'

        self.playlist_file = 'playlist.txt'
        self.playlist = list()
        if os.path.isfile(self.playlist_file):
            with open(self.playlist_file, 'r') as file:
                for line in file.readlines():
                    self.playlist.append(line.strip())

        if len(self.playlist) > 0:
            self.current_video_id = self.playlist[0]
        else:
            self.current_video_id = str()

        self.music_player = player.Player()
        try:
            self.sense_hat = sense_hat.SenseHat()
        except NameError:
            self.sense_hat = None

        self.horizontalSlider.setValue(100)
        self.horizontalSlider.valueChanged.connect(self.update_volume)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_mute.clicked.connect(self.media_mute)
        self.pushButton_play.clicked.connect(self.media_play)
        self.pushButton_pause.clicked.connect(self.media_pause)
        self.pushButton_stop.clicked.connect(self.media_stop)
        self.pushButton_search.clicked.connect(self.start_text)
        self.lineEdit.returnPressed.connect(self.start_text)
        self.pushButton_voice.clicked.connect(self.start_voice)
        self.pushButton_forwards.clicked.connect(self.media_forward)
        self.pushButton_back.clicked.connect(self.media_backward)

        if self.sense_hat is not None:
            self.sense_hat.stick.direction_up = self.volume_up
            self.sense_hat.stick.direction_down = self.volume_down
            self.sense_hat.stick.direction_left = self.media_backward
            self.sense_hat.stick.direction_right = self.media_forward

    def search_and_download(self, search_terms):
        self.current_video_id = search.search(search_terms)
        if not os.path.isfile(self.current_video_id + self.ext):
            download.download(self.current_video_id)

    def start_text(self):
        self.search_and_download(self.lineEdit.text())
        self.media_open(self.current_video_id + self.ext)
        self.media_play()

    def start_voice(self):
        transcription = speech.transcribe()
        if transcription.lower() == 'pause':
            self.media_pause()
        elif transcription.lower() == 'play':
            self.media_play()
        elif transcription.lower() == 'stop':
            self.media_stop()
        elif transcription.lower() == 'forward' or transcription.lower() == 'forwards' \
                or transcription.lower() == 'next':
            self.media_forward()
        elif transcription.lower() == 'backward' or transcription.lower() == 'backwars' \
                or transcription.lower() == 'back' or transcription.lower() == 'previous':
            self.media_backward()
        else:
            self.search_and_download(transcription)
            self.media_open(self.current_video_id + self.ext)
            self.media_play()

    def update_volume(self):
        volume = self.horizontalSlider.value() + 1
        self.music_player.set_volume(volume)
        self.label_volume.setText(str(volume) + '%')

        if self.sense_hat is not None:
            if volume < 33:
                self.sense_hat.set_pixels(icons.volume_min)
            elif volume < 66:
                self.sense_hat.set_pixels(icons.volume_med)
            else:
                self.sense_hat.set_pixels(icons.volume_max)

    def media_mute(self):
        self.music_player.mute()
        self.pushButton_mute.setText('Unmute')
        if self.sense_hat is not None:
            self.sense_hat.set_pixels(icons.mute)
        self.pushButton_mute.clicked.disconnect()
        self.pushButton_mute.clicked.connect(self.media_unmute)

    def media_unmute(self):
        self.music_player.unmute()
        self.pushButton_mute.setText('Mute')
        if self.sense_hat is not None:
            self.sense_hat.set_pixels(icons.play)
        self.pushButton_mute.clicked.disconnect()
        self.pushButton_mute.clicked.connect(self.media_mute)

    def media_play(self):
        self.music_player.play()
        self.label_status.setText('Playing')
        if self.sense_hat is not None:
            self.sense_hat.stick.direction_middle = self.media_pause
            self.sense_hat.set_pixels(icons.play)

    def media_pause(self):
        self.music_player.pause()
        self.label_status.setText('Paused')
        if self.sense_hat is not None:
            self.sense_hat.stick.direction_middle = self.media_play
            self.sense_hat.set_pixels(icons.pause)

    def media_stop(self):
        self.music_player.stop()
        self.label_status.setText('Stopped')

    def media_open(self, file):
        self.music_player.open(file)
        if not file.split(sep='.')[0] in self.playlist:
            self.add_to_playlist(file.split(sep='.')[0])

    def volume_up(self):
        volume = self.horizontalSlider.value() + 1
        self.horizontalSlider.setValue(volume + 10)

    def volume_down(self):
        volume = self.horizontalSlider.value() + 1
        self.horizontalSlider.setValue(volume - 10)

    def add_to_playlist(self, video_id):
        self.playlist.append(video_id)
        with open(self.playlist_file, 'a') as file:
            file.write(video_id + '\n')

    def media_forward(self):
        if len(self.playlist) > 0 and self.current_video_id != '':
            if self.sense_hat is not None:
                self.sense_hat.set_pixels(icons.forward)

            index = self.playlist.index(self.current_video_id)
            target_index = index + 1
            if target_index > len(self.playlist) - 1:
                target_index = len(self.playlist) - 1

            self.download_and_play(self.playlist[target_index])

    def media_backward(self):
        if len(self.playlist) > 0 and self.current_video_id != '':
            if self.sense_hat is not None:
                self.sense_hat.set_pixels(icons.backwards)

            index = self.playlist.index(self.current_video_id)
            target_index = index - 1
            if target_index < 0:
                target_index = 0

            self.download_and_play(self.playlist[target_index])

    def download_and_play(self, video_id):
        self.current_video_id = video_id
        if not os.path.isfile(self.current_video_id + self.ext):
            download.download(self.current_video_id)

        self.media_open(self.current_video_id + self.ext)
        self.media_play()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
