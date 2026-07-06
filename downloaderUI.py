from pathlib import Path
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from os import startfile, path
from downloader import Downloader
import sys
import configparser

DOWNLOAD_PATH = str(Path.home()/"Downloads")
BAD_LIST = ["\\", ":", "?", "#", "%", "&", "{", "}", "<", ">", "*", "/", "$", "!", "\'", "\"", ":", "@", "+", "`", "|", "="]

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

        # if successful, update UI
        if resultMessage[:6] != "ERROR:":
            self.gotodownloadfolderbutton.setVisible(True)
            self.resize(400, 230)
    
    def openDownloads(self):
        startfile(DOWNLOAD_PATH)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # check if ffmpeg exe is listed
    config = configparser.ConfigParser()
    config.read("config.ini")

    ffmpegPath = config["LOCATIONS"]["ffmpeg_location"]

    window = YouTubeDownloaderUI(Downloader(ffmpegPath=ffmpegPath))
    window.show()
    exit(app.exec())