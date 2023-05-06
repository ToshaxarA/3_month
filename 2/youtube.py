from pytube import YouTube
url = input("URL: ")
yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
yt.streams.filter(progressive=True, file_extension='mp4', res='720p').order_by('resolution').desc().first().download()
yt.streams.filter(only_audio=True).desc().first().download('audio', f'{yt.title}.mp3')
# https://youtu.be/ziquA0hrlag