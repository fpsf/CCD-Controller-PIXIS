"""

Author: Fernando Ferrari

Created on: ...

This file contains a class with the methods to execute all of the program's possible actions;
in other words, this is the program's main controller.

Said class requires methods from the PIXIS driver class in src/driver/pixis.py and
the camera.ini settings class on src/saving/camera_settings.py

"""

import datetime

from actions.console import ConsoleThreadOutput
from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Actions:

    def __init__(self):
        self.driver = CCDPixis()
        self.cs = CameraSettings()
        self.gain_to_driver()
        self.shoot_on = None
        self.is_connected = False
        self.console = ConsoleThreadOutput()

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
                else:
                    self.console.write_to_console("Failed to connect. PVCAM Error.", 3)
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def disconnect_cam(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        else:
            try:
                self.console.write_to_console("Disconnecting...", 0)
                self.driver.close()
                if not self.driver.error():
                    self.console.write_to_console("Disconnected Successfully.", 1)
                    self.is_connected = False
                else:
                    self.console.write_to_console("Failed to Disconnect. PVCAM Error.", 3)
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def standby(self):
        try:
            self.console.write_to_console("Entering Standby Mode...", 1)
            self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, 2500)
            # self.signal_console.emit("Success", 1)
        except Exception as e:
            self.console.write_to_console("Standby Failed: " + str(e), 3)

    def get_temp(self):
        return self.driver.get_param(self.driver.pv.PARAM_TEMP)[1]

    def shoot(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        else:
            try:
                self.shoot_on = True
                self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, int(self.cs.temp) * 100)
                temp_wait = datetime.datetime.now() + datetime.timedelta(seconds=600)
                while self.driver.get_param(self.driver.pv.PARAM_TEMP)[1] != int(self.cs.temp) * 100 and datetime.datetime.now() < temp_wait:
                    continue
                # TODO Change time unit?
                end_time = datetime.datetime.now() + datetime.timedelta(seconds=int(self.cs.time_shooting))
                while datetime.datetime.now() < end_time and self.shoot_on:
                    self.driver.take_picture(int(self.cs.binning), int(self.cs.exp), self.cs.path)
                self.console.write_to_console("Shooting Finished.", 1)
                self.standby()
            except Exception as e:
                self.console.write_to_console("Shooting Failed: " + str(e), 3)

    def stop(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        elif not self.shoot_on:
            self.console.write_to_console("Already Stopped.", 2)
        else:
            self.console.write_to_console("Stopping...", 0)
            self.shoot_on = False
            self.console.write_to_console("Stopped successfully", 1)

    def gain_to_driver(self):
        if self.driver.pvcam:
            self.cs.load_settings()
            self.driver.set_param(self.driver.pv.PARAM_GAIN_INDEX, int(self.cs.gain) + 1)
