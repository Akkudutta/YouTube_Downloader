import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import shutil
import re
import sys
import subprocess

def convert_to_audio_or_video():
    video_url = entry.get()  # Get the YouTube video URL from the entry widget
    selected_format = format_combobox.get()  # Get the selected format

    try:
        my_video = YouTube(video_url)
        cleaned_title = re.sub(r'\W+', '_', my_video.title)

        if selected_format == "audio_wav":
            audio_stream = my_video.streams.get_audio_only()
            mp4_file_path = audio_stream.download(output_path=os.path.expanduser("~/Downloads"), filename=cleaned_title)

            audio_clip = AudioFileClip(mp4_file_path)
            wav_file_path = os.path.splitext(mp4_file_path)[0] + ".wav"
            audio_clip.write_audiofile(wav_file_path)
            audio_clip.close()
            os.remove(mp4_file_path)
            result_label.config(text="WAV file downloaded successfully.")
        elif selected_format == "audio_mp3":
            audio_stream = my_video.streams.get_audio_only()
            mp4_file_path = audio_stream.download(output_path=os.path.expanduser("~/Downloads"), filename=cleaned_title)

            mp3_file_path = os.path.splitext(mp4_file_path)[0] + ".mp3"
            shutil.move(mp4_file_path, mp3_file_path)
            result_label.config(text="MP3 file downloaded successfully.")
        elif selected_format == "video":
            video_stream = my_video.streams.get_highest_resolution()
            mp4_file_path = video_stream.download(output_path=os.path.expanduser("~/Downloads"), filename=cleaned_title)
            mp4_file_path_with_extension = mp4_file_path + ".mp4"
            os.rename(mp4_file_path, mp4_file_path_with_extension)
            result_label.config(text="Video downloaded successfully.")

        #my_video.close()
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Redirect standard output and error to files
sys.stdout = open('stdout.txt', 'w')
sys.stderr = open('stderr.txt', 'w')

# Create a GUI window
window = tk.Tk()
window.title("YouTube Downloader")

# Label and Entry widget for the YouTube URL
url_label = tk.Label(window, text="Enter YouTube URL:")
url_label.pack()

entry = tk.Entry(window)
entry.pack()

# Format selection dropdown
format_label = tk.Label(window, text="Select Download Format:")
format_label.pack()

format_combobox = ttk.Combobox(window, values=["audio_wav", "audio_mp3", "video"])
format_combobox.pack()

# Download button
download_button = tk.Button(window, text="Download", command=convert_to_audio_or_video)
download_button.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

# Start the GUI event loop
window.mainloop()

# Restore standard output and error
sys.stdout.close()
sys.stderr.close()
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
