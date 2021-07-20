from os import remove
from os.path import isfile

from gtts import gTTS
import youtube_dl

from settings import DEFAULT_YOUTUBE_OPTIONS, MAX_YOUTUBE_VIDEOS, MAX_TTS_FILES


class Manager:
    def __init__(self):
        self.current_youtube_options = DEFAULT_YOUTUBE_OPTIONS
        self.cnt_yt = 0
        self.cnt_tts = 0
        self.video_map = {}
        self.delete_youtube_files()

    def delete_youtube_files(self):
        for i in range(MAX_YOUTUBE_VIDEOS):
            if isfile("yt" + str(i) + ".wav"):
                remove("yt" + str(i) + ".wav")

    def tts_query(self, text):
        tts = gTTS(text)
        result_name = "tts" + str(self.cnt_tts) + ".wav"
        self.cnt_tts = (self.cnt_tts) % MAX_TTS_FILES
        tts.save(result_name)
        return result_name

    def youtube_query(self, url):
        if url in self.video_map:
            return self.video_map[url]

        file_name = "yt" + str(self.cnt_yt) + ".wav"
        self.video_map[url] = file_name
        self.cnt_yt = (self.cnt_yt + 1) % MAX_YOUTUBE_VIDEOS
        self.current_youtube_options["outtmpl"] = file_name
        with youtube_dl.YoutubeDL(self.current_youtube_options) as ydl:
            ydl.download([url])
        return file_name
