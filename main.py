#!/usr/bin/env python3
import sys
import search
import download
import player
import speech


def main():
    argv = ' '.join(map(str, sys.argv[1:]))
    if argv != '':
        use_voice = False
    else:
        use_voice = True
    while True:
        if argv != '':
            search_terms = argv
            argv = ''
        elif not use_voice:
            search_terms = input('Music to play: ')
        else:
            print('Listening...')
            search_terms = speech.transcribe()

        video_id = search.search(search_terms)

        download.download(video_id)

        music_player = player.Player()
        music_player.open(video_id + '.flac')
        music_player.play()
        while not music_player.ended():
            pass

if __name__ == '__main__':
    main()
