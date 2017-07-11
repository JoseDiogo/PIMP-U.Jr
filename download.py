import youtube_dl


def download(video_id):
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://youtube.com/watch?v=' + video_id])
