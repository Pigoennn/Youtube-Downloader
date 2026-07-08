from src.downloader import Downloader
from src.downloaderUI import YouTubeDownloaderUI
from PyQt6.QtWidgets import QApplication, QMessageBox
import configparser
import sys
from os import path

def displayError(e: configparser.Error | KeyError):
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Icon.Critical)
    error_msg.setWindowTitle("Configuration Error")
    error_msg.setText("Your 'config.ini' file is missing, invalid, or corrupted.")
    error_msg.setInformativeText(f"Missing key details: {e}\n\nPlease check your configuration file and try again.")
    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if getattr(sys, "frozen", False):
        bundleDir = getattr(sys, "_MEIPASS", path.abspath("."))
        ffmpegDir = path.join(bundleDir, "ffmpeg")
    else:
        currentDir = path.dirname(path.abspath(__file__))
        ffmpegDir = path.join(currentDir, "src", "ffmpeg")

    config = configparser.ConfigParser()
    config.read("config.ini")

    try: 
        outputPath = config["LOCATIONS"]["download_location"]
        imageName = config["NAMES"]["image_name"]
    except (configparser.Error, KeyError) as e:
        # KeyError occurs if a section or an option is missing or misspelled
        displayError(e)
        sys.exit(1)

    window = YouTubeDownloaderUI(Downloader(outputPath, ffmpegDir), outputPath)
    window.setImage(imageName)
    window.show()
    sys.exit(app.exec())