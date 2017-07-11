import vlc

class Player():
    def open(self, file):
        self.player = vlc.MediaPlayer(file)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def mute(self):
        self.player.audio_set_mute(True)

    def unmute(self):
        self.player.audio_set_mute(False)

    def set_volume(self, volume):
        self.player.audio_set_volume(volume)
