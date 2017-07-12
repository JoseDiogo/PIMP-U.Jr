#!/usr/bin/env python3
import sys
import search
import download
import player


def main():
    search_terms = ' '.join(map(str, sys.argv[1:]))
    video_id = search.search(search_terms)

    download.download(video_id)

    music_player = player.Player()
    music_player.open(video_id + '.flac')
    music_player.play()
    while not music_player.ended():
        pass

if __name__ == '__main__':
    main()
