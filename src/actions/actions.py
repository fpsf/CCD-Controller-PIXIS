"""

Author: Fernando Ferrari

Created on: ...

This file contains a class with the methods to execute all of the program's possible actions;
in other words, this is the program's main controller.

Said class requires methods from the PIXIS driver class in src/driver/pixis.py and
the camera.ini settings class on src/saving/camera_settings.py

"""

import datetime

from PyQt5 import QtCore

from actions.console import ConsoleThreadOutput
from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Actions(CCDPixis):

    # signal_console = QtCore.pyqtSignal(str, int, name="signalConsole")

    def __init__(self):
        super().__init__()
        # super() = CCDPixis()
        # super().__init__()
        self.cs = CameraSettings()
        self.shoot_on = None
        self.is_connected = False
        self.console = ConsoleThreadOutput()

    def connect(self):
        if self.is_connected:
            self.console.write_to_console("Already Connected.", 2)
        else:
            try:
                self.console.write_to_console("Connecting...", 0)
                super().open()
                self.console.write_to_console("Connected Successfully.", 1)
                self.is_connected = True
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def disconnect_cam(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        else:
            try:
                self.console.write_to_console("Disconnecting...", 0)
                super().close()
                self.console.write_to_console("Disconnected Successfully.", 1)
                self.is_connected = False
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def standby(self):
        try:
            self.console.write_to_console("Entering Standby Mode...", 1)
            super().set_param(super().pv.PARAM_TEMP_SETPOINT, 2500)
            # self.signal_console.emit("Success", 1)
        except Exception as e:
            self.console.write_to_console("Standby Failed: " + str(e), 3)

    def get_temp(self):
        return super().get_param(super().pv.PARAM_TEMP)[1]

    def shoot(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        else:
            try:
                self.shoot_on = True
                super().set_param(super().pv.PARAM_TEMP_SETPOINT, int(self.cs.temp) * 100)
                temp_wait = datetime.datetime.now() + datetime.timedelta(seconds=600)
                while super().get_param(super().pv.PARAM_TEMP)[1] != int(self.cs.temp) * 100 and datetime.datetime.now() < temp_wait:
                    continue
                # TODO Change time unit?
                end_time = datetime.datetime.now() + datetime.timedelta(seconds=int(self.cs.time_shooting))
                while datetime.datetime.now() < end_time and self.shoot_on:
                    super().take_picture(int(self.cs.binning), int(self.cs.exp), self.cs.path)
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
