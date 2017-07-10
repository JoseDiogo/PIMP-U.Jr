import youtube_dl

def download(link):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
