import ffmpeg
from tkinter import filedialog

video_path = filedialog.askopenfilename(title="Select Video", filetypes=[("MP4 files", "*.mp4"), ("MKV Files", "*.mkv"), ("All Files", "*.*")])
audio_path = filedialog.askopenfilename(title="Select Audio", filetypes=[("MP3 files", "*.mp3"), ("M4A Files", "*.m4a"), ("All Files", "*.*")])

video_stream = ffmpeg.input(video_path)
audio_stream = ffmpeg.input(audio_path)

ffmpeg.output(audio_stream, video_stream, 'out.mp4').run()