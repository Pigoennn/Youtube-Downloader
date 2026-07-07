from src.downloader import Downloader
from src.downloaderUI import YouTubeDownloaderUI
from PyQt6.QtWidgets import QApplication
import configparser
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config = configparser.ConfigParser()
    config.read("config.ini")

    # check if download path is listed
    outputPath = config["LOCATIONS"]["download_location"]
    # check if ffmpeg.exe path is listed
    ffmpegPath = config["LOCATIONS"]["ffmpeg_location"]

    imageName = config["NAMES"]["image_name"]

    window = YouTubeDownloaderUI(Downloader(outputPath, ffmpegPath))
    window.setImage(imageName)
    window.show()
    exit(app.exec())