from pytube import YouTube
#from pytubefix import YouTube
from pathlib import Path
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from os import startfile, path
import sys

downloadpath = str(Path.home()/"Downloads")
badlist = ["\\", ":", "?", "#", "%", "&", "{", "}", "<", ">", "*", "/", "$", "!", "\'", "\"", ":", "@", "+", "`", "|", "="]

def findimage(original: str):
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
                if any(i in title for i in badlist):
                    for j in badlist:
                        title = title.replace(j, "")
                stream.download(output_path=downloadpath, filename = title + '.mp3')
                return "Done!"
            except Exception as Error:
                print(Error)
                return f'Oopie: {Error}'
        case _:
            return "Bro choose mp3 or mp4"

class YouTubeDownloader(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("YouTube Video Downloader")
        self.setWindowIcon(QIcon(findimage("shocku.png")))
        self.createradiobuttons()
        self.createurlinput()
        self.createlabels()
        self.createpushbuttons()

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

    def createurlinput(self):
        self.urlbox = QLineEdit()
        self.urlbox.setFixedWidth(150)
        #self.urlbox.setFixedSize(150,60)
        self.urlbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.urlbox.textChanged.connect(self.update)
    
    def createlabels(self):
        self.titlelabel = QLabel("<h2>Jono's Really Cool Video Downloader</h2>")
        self.mplabel = QLabel("<h3>Choose File Type:</h3>")
        self.urllabel = QLabel("<h3>URL</h3>")
        self.errorlabel = QLabel("")
        self.errorlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def createpushbuttons(self):
        self.downloadbutton = QPushButton("Download")
        self.downloadbutton.clicked.connect(self.downloading)
        self.downloadbutton.setFixedSize(200,30)
        self.gotodownloadfolderbutton = QPushButton("Go to Downloads Folder")
        self.downloadbutton.setFixedSize(175, 25)
        self.gotodownloadfolderbutton.setVisible(False)
        self.gotodownloadfolderbutton.clicked.connect(self.opendownloads)

    def createradiobuttons(self):
        self.mp3button = QRadioButton("MP3", self)
        self.mp3button.toggled.connect(self.optionselected)

        self.mp4button = QRadioButton("MP4", self)
        self.mp4button.toggled.connect(self.optionselected)

    def optionselected(self):
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
    
    def opendownloads(self):
        startfile(downloadpath)

from sys import argv, exit

app = QApplication(argv)
window = YouTubeDownloader()
window.show()
exit(app.exec())