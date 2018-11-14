"""

Author: Fernando Ferrari

Created on: ...

This file contains a class with the methods to execute all of the program's possible actions;
in other words, this is the program's main controller.

Said class requires methods from the PIXIS driver class in src/driver/pixis.py and
the camera.ini settings class on src/saving/camera_settings.py

"""
import datetime
import time

from actions.console import ConsoleThreadOutput
from actions.shooter import Shooter
from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Actions:

    def __init__(self):
        self.driver = CCDPixis()
        self.cs = CameraSettings()

        self.is_connected = False
        self.console = ConsoleThreadOutput()

        self.shooter = Shooter()
        self.shooter.taking_picture.connect(self.picnumber)
        self.shooter.pvcam_failure.connect(self.pvcam_failure)
        self.shooter.shooting_failure.connect(self.shooting_failure)
        self.shooter.finished.connect(self.shooting_finished)

    def picnumber(self):
        self.console.write_to_console("Acquiring Image: " + str(self.shooter.pic_counter), 1)

    def pvcam_failure(self):
        self.console.write_to_console("Shooting Failed: PVCAM Error.", 3)
        time.sleep(1)
        self.console.write_to_console("Aborting...", 3)
        time.sleep(1)
        self.standby()

    def shooting_failure(self):
        self.console.write_to_console("Shooting Failed: Shooter Thread Exception.", 3)
        time.sleep(1)
        self.console.write_to_console("Aborting...", 3)
        time.sleep(1)
        self.standby()

    def shooting_finished(self):
        self.console.write_to_console("Shooting Finished.", 1)
        self.standby()

    def standby(self):
        try:
            self.console.write_to_console("Entering Standby Mode.", 1)
            self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, 2500)
            # self.signal_console.emit("Success", 1)
        except Exception as e:
            self.console.write_to_console("Standby Failed: " + str(e), 3)

    def connect(self):
        if self.is_connected:
            self.console.write_to_console("Already Connected.", 2)
        else:
            try:
                self.console.write_to_console("Connecting...", 0)
                self.driver.open()
                if not self.driver.error():
                    self.console.write_to_console("Connected Successfully.", 1)
                    self.is_connected = True
                    self.standby()
                    self.gain_to_driver()
                else:
                    self.console.write_to_console("Failed to connect. PVCAM Error.", 3)
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def disconnect_cam(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        elif self.shooter.isRunning():
            self.console.write_to_console("Unavailable During acquisition.", 2)
        else:
            try:
                self.console.write_to_console("Disconnecting...", 0)
                self.standby()
                self.driver.close()
                if not self.driver.error():
                    self.console.write_to_console("Disconnected Successfully.", 1)
                    self.is_connected = False
                else:
                    self.console.write_to_console("Failed to Disconnect. PVCAM Error.", 3)
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def get_temp(self):
        return self.driver.get_param(self.driver.pv.PARAM_TEMP)[1]

    def shoot(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        elif self.shooter.isRunning():
            self.console.write_to_console("Camera Already Running.", 2)
        else:
            self.console.write_to_console("Preparing Acquisition...", 0)
            self.shooter.start()
            '''
            pcacts = self.shooter.pic_counter
            while not self.shooter.shoot_on:
                continue
            while self.shooter.shoot_on:
                if pcacts < self.shooter.pic_counter:
                    self.console.write_to_console("\n", 0)
                    self.console.write_to_console("Image: " + str(pcacts) + "Acquired.", 1)
                    self.console.write_to_console("Acquisition Time Remaining:" +
                                                  str(self.shooter.end_time - datetime.datetime.now()) + "s", 1)
                    self.console.write_to_console("Current Temperature: " +
                                                  "{0:.2f}".format(self.get_temp() / 100, 0), 1)
                    self.console.write_to_console("Waiting " + str(self.cs.acq_wait) + "s For Next Image...", 1)
                    pcacts = self.shooter.pic_counter
                elif self.shooter.pvcam_failure:
                    self.console.write_to_console("\n", 0)
                    self.console.write_to_console("Shooting Failed: PVCAM Error", 3)
                    self.console.write_to_console("Aborting...", 3)
            if not self.shooter.shooting_failure and not self.shooter.shoot_on:
                self.console.write_to_console("Shooting Finished.", 1)
                self.console.write_to_console("Entering Standby Mode.", 1)
            else:
                self.console.write_to_console("Shooting Failed: Shooter Thread Exception.", 3)
            '''

    def stop(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        elif not self.shooter.isRunning():
            self.console.write_to_console("Already Stopped.", 2)
        else:
            if self.shooter.shoot_on:
                self.shooter.shoot_on = False
            self.console.write_to_console("Stopping...", 0)
            self.standby()
            self.console.write_to_console("Stopped successfully", 1)

    def gain_to_driver(self):
        if self.driver.pvcam:
            self.cs.load_settings()
            self.driver.set_param(self.driver.pv.PARAM_GAIN_INDEX, int(self.cs.gain) + 1)
