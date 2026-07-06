from typing import Any
import yt_dlp

class Downloader:
    """
    Class to manage downloading files of a given type from a given link 
    """
    outputPath: str
    baseConfig: dict[str, Any]
    ydlConfig: dict[str, Any]

    def __init__(self, outputPath: str = ".", ffmpegPath: str | None = None) -> None:
        self.outputPath = outputPath
        self.baseConfig = {
            "outtmpl": f"{outputPath}/%(title)s.%(ext)s"
        }
        self.ydlConfig: dict[str, Any] = {}

        if (ffmpegPath):
            self.baseConfig["ffmpeg_location"] = ffmpegPath
            
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