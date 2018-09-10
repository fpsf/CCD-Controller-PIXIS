import configparser
import os


class CameraSettings:
    def __init__(self):
        self.gain = None

        self.temp = None

        self.time_shooting = None
        self.acq_wait = None

        self.binning = None
        self.exp = None
        self.path = None

        self.config = configparser.ConfigParser()

        self.load_settings()

    def load_settings(self):
        self.config.read(os.getcwd() + "camera")
        self.gain = self.config["Camera"]["Gain"]
        self.temp = self.config["Camera"]["Temperature"]
        self.time_shooting = self.config["Camera"]["ShootingTime"]
        self.acq_wait = self.config["Camera"]["TimeBetweenPhotos"]
        self.binning = self.config["Camera"]["Binning"]
        self.exp = self.config["Camera"]["ExposureTime"]
        self.path = self.config["Camera"]["ImagesPath"]

    def save_settings(self):
        self.config["Camera"]["Gain"] = self.gain
        self.config["Camera"]["Temperature"] = self.temp
        self.config["Camera"]["ShootingTime"] = self.time_shooting
        self.config["Camera"]["TimeBetweenPhotos"] = self.acq_wait
        self.config["Camera"]["Binning"] = self.binning
        self.config["Camera"]["ExposureTime"] = self.exp
        self.config["Camera"]["ImagesPath"] = self.path
        with open(os.getcwd() + "camera") as configfile:
            self.config.write(configfile)
