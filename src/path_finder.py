from os import path
import sys
import configparser

class PathFinder:
    isFrozen: bool
    config: configparser.ConfigParser

    def __init__(self, isFrozen: bool):
        self.isFrozen = isFrozen
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def getFFMPEG(self) -> str:
        """ Finds the path resolution of the ffmpeg executable. """
        if self.isFrozen:
            bundleDir = getattr(sys, "_MEIPASS", path.abspath("."))
            ffmpegDir = path.join(bundleDir, "ffmpeg")
        else:
            currentDir = path.dirname(path.abspath(__file__))
            ffmpegDir = path.join(currentDir, "ffmpeg")
        
        return ffmpegDir
    
    def getOutputFolder(self) -> str | configparser.Error | KeyError:
        """ Finds the path resolution of the output folder. """
        try:
            return self.config.get("LOCATIONS", "download_location")
        except (configparser.Error, KeyError) as e:
            return e
    
    def getImagePath(self) -> str | configparser.Error | KeyError:
        """ Finds the path resolution of the image. """
        try:
            return self.config.get("NAMES", "image_name")
        except (configparser.Error, KeyError) as e:
            return e