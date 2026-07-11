from src.downloader import Downloader
from src.downloaderUI import YouTubeDownloaderUI
from src.path_finder import PathFinder
from PyQt6.QtWidgets import QApplication, QMessageBox
import configparser
import sys
from typing import NoReturn

def getVerifiedPath(instance: str | configparser.Error | KeyError) -> str | NoReturn:
    """
    Ensures the path is valid.
    Returns the path as a `str` if valid, or displays an error window and
    ends the application when the user is done.
    """
    if isinstance(instance, (configparser.Error, KeyError)):
        displayError(instance)
        sys.exit(1)
    else:
        return str(instance)
    
def displayError(e: configparser.Error | KeyError) -> None:
    """ Displays the error window. """
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Icon.Critical)
    error_msg.setWindowTitle("Configuration Error")
    error_msg.setText("Your 'config.ini' file is missing, invalid, or corrupted.")
    error_msg.setInformativeText(f"Missing key details: {e}\n\nPlease check your configuration file and try again.")
    error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    error_msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pathFinder = PathFinder(getattr(sys, "_MEIPASS", False))

    outputPath = getVerifiedPath(pathFinder.getOutputFolder())
    imagePath = getVerifiedPath(pathFinder.getImagePath())

    ffmpegDir = pathFinder.getFFMPEG()

    window = YouTubeDownloaderUI(Downloader(outputPath, ffmpegDir), outputPath)
    window.setImage(imagePath)
    window.show()
    sys.exit(app.exec())