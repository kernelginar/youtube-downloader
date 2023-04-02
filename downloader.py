import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar, QComboBox
from pytube import YouTube

class YoutubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        # Title
        self.setWindowTitle("YouTube Video Downloader")

        # Create Widgets
        url_label = QLabel("Video URL:")
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Enter video URL here...")
        self.format_label = QLabel("Video Format:")
        self.format_btn = QPushButton("Download as Video")
        self.audio_btn = QPushButton("Download as Audio")
        self.save_label = QLabel("Save As:")
        self.save_edit = QLineEdit()
        self.save_edit.setPlaceholderText("Enter file name...")
        self.extension_label = QLabel("Extension:")
        self.extension_edit = QLineEdit()
        self.extension_edit.setPlaceholderText("Enter file extension...")
        self.resolution_label = QLabel("Resolution:")
        self.resolution_combobox = QComboBox()
        self.download_btn = QPushButton("Download")
        self.progress_bar = QProgressBar()

        # Set Connections
        self.format_btn.clicked.connect(self.show_resolutions)
        self.audio_btn.clicked.connect(self.download_audio)
        self.download_btn.clicked.connect(self.download)
        self.progress_bar.setValue(0)

        # Create layout
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(url_label)
        hbox1.addWidget(self.url_edit)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.format_label)
        hbox2.addWidget(self.format_btn)
        hbox2.addWidget(self.audio_btn)
        vbox.addLayout(hbox2)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.resolution_label)
        hbox3.addWidget(self.resolution_combobox)
        vbox.addLayout(hbox3)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.save_label)
        hbox4.addWidget(self.save_edit)
        hbox4.addWidget(self.extension_label)
        hbox4.addWidget(self.extension_edit)
        vbox.addLayout(hbox4)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.download_btn)
        vbox.addWidget(self.progress_bar)
        # Add Layout to main widget
        self.setLayout(vbox)
        
        # Define audio property
        self.audio = False

    # Function of Download Video
    def download_video(self):
        self.audio = False
        self.show_resolutions()

    # Function of Download Audio
    def download_audio(self):
        self.audio = True
        self.show_resolutions()

    # Function to Show resolutions
    def show_resolutions(self):
        # Create YouTube video object
        self.video = YouTube(self.url_edit.text())

        # Add resolutions to combobox
        self.resolution_combobox.clear()
        if self.audio:
            self.resolution_combobox.addItem("Audio Only")
        else:
            streams = self.video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()
            for stream in streams:
                resolution = f"{stream.resolution} - {stream.fps}fps"
                self.resolution_combobox.addItem(resolution)

    # Function of Download File
    def download(self):
        # Input Control
        if not self.url_edit.text():
            print("Please enter a valid URL.")
           
    # Video Download Function
    def download_video(self):
        self.audio = False
        self.resolution_combobox.clear() # clear old options in combobox
        # get the resolutions of all downloadable videos and add them to the combobox
        video_streams = self.video.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()
        for stream in video_streams:
            resolution = f"{stream.resolution} ({stream.fps} fps)"
            self.resolution_combobox.addItem(resolution)

    # Audio File Download Function
    def download_audio(self):
        self.audio = True
        self.resolution_combobox.clear() # clear old options in combobox

    # File Download Function
    def download(self):
        # Input Control
        if not self.url_edit.text():
            print("Please enter a valid URL.")
            return
        if not self.save_edit.text():
            print("Please enter a file name.")
            return
        if not self.extension_edit.text():
            print("Please enter a file extension.")
            return

        # Create YouTube video object
        self.video = YouTube(self.url_edit.text())

        # Create the file name and extension to download
        self.filename = self.save_edit.text() + '.' + self.extension_edit.text()

        # Start the Download
        self.video.register_on_progress_callback(self.show_progress)
        if self.audio:
            self.video.streams.filter(only_audio=True).first().download(filename=self.filename)
        else:
            # Download video according to the resolution selected from the combobox
            selected_resolution = self.resolution_combobox.currentText().split()[0]
            self.video.streams.filter(adaptive=True, file_extension='mp4', resolution=selected_resolution).first().download(filename=self.filename)

    # Show download progress
    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size * 100
        self.progress_bar.setValue(int(percentage))
        self.progress_bar.update()

# Start the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    downloader = YoutubeDownloader()
    downloader.show()
    sys.exit(app.exec_())
