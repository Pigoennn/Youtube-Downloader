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

downloadPath = str(Path.home()/"Downloads")
BAD_LIST = ["\\", ":", "?", "#", "%", "&", "{", "}", "<", ">", "*", "/", "$", "!", "\'", "\"", ":", "@", "+", "`", "|", "="]

def findImage(original: str):
    try:
        basepath = sys._MEIPASS
    except AttributeError:
        basepath = path.abspath(".")
        relativepath = original
    else:
        mainthing = path.split(original)[1]
        relativepath = mainthing
    return path.join(basepath, relativepath)

def downloader(filetype: str, link: str):
    youtubevideoobject = YouTube(link)
    '''try:
        youtubevideoobject = YouTube(link)
    except Exception as Error:
        return f"You made an oopsie: {Error}"'''
    match filetype:
        case "mp4":    
            youtubevideoobject = youtubevideoobject.streams.get_highest_resolution()
            try:
                youtubevideoobject.download(output_path = downloadpath)
                return "Done!"
            except Exception as Error:
                return f'Oopie: {Error}'
        case "mp3":
            try:
                stream = youtubevideoobject.streams.filter(only_audio = True).first()
                title = str(youtubevideoobject.title)
                if any(i in title for i in BAD_LIST):
                    for j in BAD_LIST:
                        title = title.replace(j, "")
                stream.download(output_path=downloadpath, filename = title + '.mp3')
                return "Done!"
            except Exception as Error:
                print(Error)
                return f'Oopie: {Error}'
        case _:
            return "Bro choose mp3 or mp4"

class Downloader:
    downloadType: str

    def __init__(self) -> None:
        pass

    def setConfig(self, downloadType: str, outputPath: str = ".") -> bool:
        ydlConfig: dict[str, Any] = {
            "outtmpl": f"{outputPath}/%(title)s.%(ext)s",
        } 
        
        match downloadType:
            case "mp3":
                ydlConfig["format"] = "bestaudio/best"
                ydlConfig["postprocessors"] = [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                }]
            case "mp4":
                ydlConfig["format"] = "bestvideo+bestaudio/best"
                ydlConfig["merge_output_format"] = "mp4"
            case _:
                return False
        
        return True

    def download(self, url: str) -> str:
        with yt_dlp.YoutubeDL(ydlConfig) as ydl:        # type: ignore
            try:
                ydl.download([url])
            except Exception as e:
                return f"ERROR: {e}"
        return "Downloaded!"

class YouTubeDownloaderUI(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("YouTube Video Downloader")
        self.setWindowIcon(QIcon(findImage("shocku.png")))
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
        if not(self.mp3button.isChecked() or self.mp4button.isChecked()):
            return self.errorlabel.setText("You have not chosen a File Type")
        elif self.urlbox.text() == "":
            return self.errorlabel.setText("You have not input a URL")

        self.errorlabel.setText("Loading...")
        string = downloader(self.mpoption.lower(), self.urlbox.text())
        self.errorlabel.setText("")
        if string == "Done!":
            self.errorlabel.setText(string)
            self.gotodownloadfolderbutton.setVisible(True)
            self.resize(400, 230)
        else:
            self.errorlabel.setText(string)
    
    def openDownloads(self):
        startfile(downloadpath)

from sys import argv, exit

app = QApplication(argv)
window = YouTubeDownloaderUI()
window.show()
exit(app.exec())