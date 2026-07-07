from pathlib import Path
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from os import startfile, path
from src.downloader import Downloader
import sys

DOWNLOAD_PATH = str(Path.home()/"Downloads")
BAD_LIST = ["\\", ":", "?", "#", "%", "&", "{", "}", "<", ">", "*", "/", "$", "!", "\'", "\"", ":", "@", "+", "`", "|", "="]
ERROR_PREFIX = "ERROR: "

class YouTubeDownloaderUI(QWidget):
    def __init__(self, downloader: Downloader) -> None:
        super().__init__()

        self.downloader = downloader

        self.setWindowTitle("YouTube Video Downloader")
        self._createRadioButtons()
        self._createURLInput()
        self._createLabels()
        self._createPushButtons()

        self.setFixedSize(400, 200)

        self.fullLayout = QVBoxLayout()
        self.configurationArea = QHBoxLayout()
        self.radioButtonLayout = QVBoxLayout()
        self.urlLayout = QVBoxLayout()

        self.fullLayout.addWidget(self.titleLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.fullLayout.addLayout(self.configurationArea)

        self.configurationArea.addLayout(self.radioButtonLayout)
        self.radioButtonLayout.addWidget(self.fileTypeLabel)
        self.radioButtonLayout.addWidget(self.mp3Button)
        self.radioButtonLayout.addWidget(self.mp4Button)

        self.configurationArea.addLayout(self.urlLayout)
        self.urlLayout.addWidget(self.urlLabel)
        self.urlLayout.addWidget(self.urlBox)

        self.fullLayout.addWidget(self.errorLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.fullLayout.addWidget(self.downloadButton, alignment=Qt.AlignmentFlag.AlignCenter)
        self.fullLayout.addWidget(self.folderRedirectionButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.fullLayout)

    def _getAbsolutePath(self, relative_path: str) -> str:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            basePath = getattr(sys, '_MEIPASS')
        except AttributeError:
            basePath = path.abspath(".")

        return path.join(basePath, relative_path)
    
    def setImage(self, imageName: str) -> None:
        """ Set the image of the application. """
        # figure out first which path to use
        if getattr(sys, "frozen", False):
            basePath = getattr(sys, "_MEIPASS", path.abspath("."))
            imagePath = path.join(basePath, imageName)
        else:
            basePath = path.dirname(path.dirname(path.abspath(__file__)))
            imagePath = path.join(basePath, imageName)
            
        self.setWindowIcon(QIcon(imagePath))

    def _createURLInput(self) -> None:
        """ Create the input box for URLs """
        self.urlBox = QLineEdit()
        self.urlBox.setFixedWidth(150)
        #self.urlBox.setFixedSize(150,60)
        self.urlBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.urlBox.textChanged.connect(self.update)
    
    def _createLabels(self) -> None:
        """ Create the title and instruction labels """
        self.titleLabel = QLabel("<h2>Jono's Really Cool Video Downloader</h2>")
        self.fileTypeLabel = QLabel("<h3>Choose File Type:</h3>")
        self.urlLabel = QLabel("<h3>URL</h3>")
        self.errorLabel = QLabel("")
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def _createPushButtons(self) -> None:
        """ Create the push buttons """
        self.downloadButton = QPushButton("Download")
        self.downloadButton.clicked.connect(self._download)
        self.downloadButton.setFixedSize(200,30)
        self.folderRedirectionButton = QPushButton("Go to Downloads Folder")
        self.downloadButton.setFixedSize(175, 25)
        self.folderRedirectionButton.setVisible(False)
        self.folderRedirectionButton.clicked.connect(self._openDownloads)

    def _createRadioButtons(self) -> None:
        """ Create the Radio Selection Buttons """
        self.mp3Button = QRadioButton("MP3", self)
        self.mp3Button.toggled.connect(self._optionSelected)

        self.mp4Button = QRadioButton("MP4", self)
        self.mp4Button.toggled.connect(self._optionSelected)

        self.fileTypeOption = ""        # set to empty to start

    def _optionSelected(self) -> None:
        """ Function called to get value of the radio selection options """
        self.fileTypeOption = self.sender().text()      # type: ignore

    def _update(self) -> None:
        """
        Called when a URL has been inputted.
        Resets the app to look clean.
        """
        self.errorLabel.setText("")
        self.folderRedirectionButton.setVisible(False)
        self.setFixedSize(400, 200)

    def _download(self) -> None:
        """ Function called to attempt to download the file type from the given URL """
        self.errorLabel.setText("")
        
        url: str = self.urlBox.text()
        if url == "":
            self.errorLabel.setText("URL Missing")
            return
        
        # set up the config
        resultMessage = self.downloader.setConfig(self.fileTypeOption.lower())
        if resultMessage != "":
            self.errorLabel.setText(resultMessage)
            return

        # attempt to download
        self.errorLabel.setText("Loading...")
        resultMessage = self.downloader.download(url)
        self.errorLabel.setText(resultMessage)

        # if successful, update UI
        if resultMessage[:len(ERROR_PREFIX)] != ERROR_PREFIX:
            self.folderRedirectionButton.setVisible(True)
            self.setFixedSize(400, 230)
    
    def _openDownloads(self) -> None:
        """ Function called to open the downloads folder. """
        startfile(DOWNLOAD_PATH)