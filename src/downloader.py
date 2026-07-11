from typing import Any
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError, GeoRestrictedError
from os import path
from typing import Any

ERROR_PREFIX = "ERROR: "

class Downloader:
    """
    Class to manage downloading files of a given type from a given link 
    """
    outputPath: str
    baseConfig: dict[str, Any]
    ydlConfig: dict[str, Any]

    def __init__(self, outputPath: str, ffmpegDir: str) -> None:
        # get output location
        self.outputPath = outputPath

        self.ydlConfig: dict[str, Any] = {}
        self.baseConfig = {
            "outtmpl": path.join(self.outputPath, "%(title)s.%(ext)s"),
            "ffmpeg_location": ffmpegDir,
            "noplaylist": True
        }
            
    def setConfig(self, downloadType: str) -> str:
        """
        Set up the config according to the given download type.
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
                currentConfig["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                currentConfig["merge_output_format"] = "mp4"
                currentConfig["remux_video"] = "mp4"
                currentConfig["postprocessors"] = [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }]
                currentConfig["postprocessor_args"] = {
                        "ExtractAudio": [
                            "-c:v", "copy",
                            "-c:a", "aac"
                        ]
                    }
            case _:
                return "Choose a file type"
            
        self.ydlConfig = currentConfig
        return ""

    def download(self, url: str, progressHook: Any = None) -> str:
        """
        Download the file format from the given url.
        All config settings must be set first.
        """
        if not self._canDownload():
            return ERROR_PREFIX + "Configuration not set. Set the configurations first."
        
        # hook
        runtimeConfig = self.ydlConfig.copy()
        if progressHook:
            runtimeConfig["progress_hooks"] = [progressHook]

        with yt_dlp.YoutubeDL(runtimeConfig) as ydl:        # type: ignore
            try:
                ydl.download([url])
            except GeoRestrictedError as e:
                return ERROR_PREFIX + "Video is geo-restricted."
            except DownloadError as e:
                return ERROR_PREFIX + "Link is invalid or is unsupported by this application."
            except ExtractorError as e:
                return ERROR_PREFIX + "YouTube is being really goofy."
            except Exception as e:
                return f"{ERROR_PREFIX}{e}"
        return "Downloaded!"
    
    def _canDownload(self) -> bool:
        """Checks that all config settings have been set."""
        requiredFeatures = ["format"]       # can add more later
        return set(requiredFeatures).issubset(self.ydlConfig.keys())