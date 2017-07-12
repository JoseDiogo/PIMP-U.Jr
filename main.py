#!/usr/bin/env python3
import search
import download
import player


def main():
    while True:
        search_terms = input('Music to play: ')
        video_id = search.search(search_terms)

        download.download(video_id)

        music_player = player.Player()
        music_player.open(video_id + '.flac')
        music_player.play()
        while not music_player.ended():
            pass

if __name__ == '__main__':
    main()
