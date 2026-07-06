from pytube import YouTube
#from pytubefix import YouTube

import yt_dlp
from typing import Any
from pathlib import Path
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from os import startfile, path
import sys

DOWNLOAD_PATH = str(Path.home()/"Downloads")
BAD_LIST = ["\\", ":", "?", "#", "%", "&", "{", "}", "<", ">", "*", "/", "$", "!", "\'", "\"", ":", "@", "+", "`", "|", "="]

class Downloader:
    """
    Class to manage downloading files of a given type from a given link 
    """
    outputPath: str
    baseConfig: dict[str, Any]
    ydlConfig: dict[str, Any]

    def __init__(self, outputPath: str = ".") -> None:
        self.outputPath = outputPath
        self.baseConfig = {
            "outtmpl": f"{outputPath}/%(title)s.%(ext)s"
        }
        self.ydlConfig: dict[str, Any] = {}

    def setConfig(self, downloadType: str) -> str:
        """
        Set the config from the given download type.
        Returns an error code if an error occurs, otherwise returns an empty string.
        """
        currentConfig = self.baseConfig.copy()      # set as temporary for now
        match downloadType:
            case "mp3":
                currentConfig["format"] = "bestaudio/best"
                currentConfig["postprocessors"] = [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                }]
            case "mp4":
                currentConfig["format"] = "bestvideo+bestaudio/best"
                currentConfig["merge_output_format"] = "mp4"
            case _:
                return "Choose a file type"
            
        self.ydlConfig = currentConfig
        return ""

    def download(self, url: str) -> str:
        """
        Download the file format from the given url.
        All config settings must be set first.
        """
        if not self.canDownload():
            return "ERROR: Configuration not set. Set the configurations first."
        
        with yt_dlp.YoutubeDL(self.ydlConfig) as ydl:        # type: ignore
            try:
                ydl.download([url])
            except Exception as e:
                return f"ERROR: {e}"
        return "Downloaded!"
    
    def canDownload(self) -> bool:
        """Checks that all config settings have been set."""
        requiredFeatures = ["format"]       # can add more later
        return set(requiredFeatures).issubset(self.ydlConfig.keys())

class YouTubeDownloaderUI(QWidget):
    def __init__(self, downloader: Downloader) -> None:
        super().__init__()

        self.downloader = downloader

        self.setWindowTitle("YouTube Video Downloader")
        self.setWindowIcon(QIcon(self.findImage("shocku.png")))
        self.createRadioButtons()
        self.createURLInput()
        self.createLabels()
        self.createPushButtons()

        self.resize(400,200)

        self.totallayout = QVBoxLayout()
        self.optionarea = QHBoxLayout()
        self.radiolayout = QVBoxLayout()
        self.urllayout = QVBoxLayout()

        self.totallayout.addWidget(self.titlelabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.totallayout.addLayout(self.optionarea)

        self.optionarea.addLayout(self.radiolayout)
        self.radiolayout.addWidget(self.mplabel)
        self.radiolayout.addWidget(self.mp3button)
        self.radiolayout.addWidget(self.mp4button)

        self.optionarea.addLayout(self.urllayout)
        self.urllayout.addWidget(self.urllabel)
        self.urllayout.addWidget(self.urlbox)

        self.totallayout.addWidget(self.errorlabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totallayout.addWidget(self.downloadbutton, alignment=Qt.AlignmentFlag.AlignCenter)
        self.totallayout.addWidget(self.gotodownloadfolderbutton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.totallayout)

    def findImage(self, relative_path: str) -> str:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = getattr(sys, '_MEIPASS')
        except AttributeError:
            base_path = path.abspath(".")

        return path.join(base_path, relative_path)

    def createURLInput(self):
        self.urlbox = QLineEdit()
        self.urlbox.setFixedWidth(150)
        #self.urlbox.setFixedSize(150,60)
        self.urlbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.urlbox.textChanged.connect(self.update)
    
    def createLabels(self):
        self.titlelabel = QLabel("<h2>Jono's Really Cool Video Downloader</h2>")
        self.mplabel = QLabel("<h3>Choose File Type:</h3>")
        self.urllabel = QLabel("<h3>URL</h3>")
        self.errorlabel = QLabel("")
        self.errorlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def createPushButtons(self):
        self.downloadbutton = QPushButton("Download")
        self.downloadbutton.clicked.connect(self.downloading)
        self.downloadbutton.setFixedSize(200,30)
        self.gotodownloadfolderbutton = QPushButton("Go to Downloads Folder")
        self.downloadbutton.setFixedSize(175, 25)
        self.gotodownloadfolderbutton.setVisible(False)
        self.gotodownloadfolderbutton.clicked.connect(self.openDownloads)

    def createRadioButtons(self):
        self.mp3button = QRadioButton("MP3", self)
        self.mp3button.toggled.connect(self.optionSelected)

        self.mp4button = QRadioButton("MP4", self)
        self.mp4button.toggled.connect(self.optionSelected)

    def optionSelected(self):
        self.mpoption = self.sender().text()

    def update(self):
        self.errorlabel.setText("")
        self.gotodownloadfolderbutton.setVisible(False)

    def downloading(self):
        self.errorlabel.setText("")
        
        url: str = self.urlbox.text()
        if url == "":
            self.errorlabel.setText("URL Missing")
            return
        
        # set up the config
        resultMessage = self.downloader.setConfig(self.mpoption.lower())
        if resultMessage != "":
            self.errorlabel.setText(resultMessage)
            return

        # attempt to download
        self.errorlabel.setText("Loading...")
        resultMessage = self.downloader.download(url)
        self.errorlabel.setText(resultMessage)

        # If successful, update UI
        if resultMessage[:6] != "ERROR:":
            self.gotodownloadfolderbutton.setVisible(True)
            self.resize(400, 230)
    
    def openDownloads(self):
        startfile(DOWNLOAD_PATH)

from sys import argv, exit

app = QApplication(argv)
window = YouTubeDownloaderUI(Downloader())
window.show()
exit(app.exec())