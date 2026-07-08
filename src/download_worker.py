from PyQt6.QtCore import QThread, pyqtSignal
from src.downloader import Downloader

class DownloadWorker(QThread):
    """
    Class to represent the Worker thread that will run in the background so the
    UI still remains interactive.
    """
    progressUpdated = pyqtSignal(int)
    statusUpdated   = pyqtSignal(str)
    finished        = pyqtSignal(str)

    downloader: Downloader
    url: str
    fileType: str

    def __init__(self, downloader: Downloader, url: str, fileType: str):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.fileType = fileType

    def run(self):
        """ Executes the download and post-processing cycle through a background thread. """

        # check user has picked a proper download before attempting to download
        resultMessage = self.downloader.setConfig(self.fileType.lower())
        if resultMessage != "":
            self.finished.emit(resultMessage)
            return

        def hook(d: dict):
            """
            Sends calculated download percentage to main GUI thread
            on every chunk download using Qt Signals.
            """
            if d["status"] == "downloading":
                # calculate percentage via downloaded / total * 100
                totalBytes = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloadedBytes = d.get("downloaded_bytes", 0)
                percentage = int((downloadedBytes / totalBytes) * 100)

                self.progressUpdated.emit(percentage)
            
            elif d["status"] == "finished":
                self.statusUpdated.emit("Finished!")

        result = self.downloader.download(self.url, hook)
        self.finished.emit(result)