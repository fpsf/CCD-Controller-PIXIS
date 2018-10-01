"""

Author: Fernando Ferrari

Created on: ...

This file contains a class with the methods to execute all of the program's possible actions;
in other words, this is the program's main controller.

Said class requires methods from the PIXIS driver class in src/driver/pixis.py and
the camera settings class on src/saving/camera_settings.py

"""

import datetime

from PyQt5 import QtCore

from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Actions(CCDPixis):

    signal_console = QtCore.pyqtSignal(name="signalConsole")

    def __init__(self):
        super().__init__()
        self.cs = CameraSettings()
        self.shoot_on = None

    def connect(self):
        self.signal_console.emit("Connecting...", 2)
        super().open()
        if not super()._error():
            self.signal_console.emit("Connected Successfully.", 1)
        else:
            self.signal_console.emit("Connection Error...", 3)

    def disconnect(self):
        self.signal_console.emit("Disconnecting...", 2)
        super().close()
        if not super()._error():
            self.signal_console.emit("Disconnected Successfully.", 1)
        else:
            self.signal_console.emit("Connection Error...", 3)

    def standby(self):
        self.signal_console.emit("Entering Standby Mode...", 1)
        super().set_param(super().pv.PARAM_TEMP_SETPOINT, 2500)
        # self.signal_console.emit("Success", 1)

    def get_temp(self):
        return super().get_param(super().pv.PARAM_TEMP)[1]

    def shoot(self):
        self.shoot_on = True
        super().set_param(super().pv.PARAM_TEMP_SETPOINT, self.cs.temp * 100)
        temp_wait = datetime.datetime.now() + datetime.timedelta(seconds=600)
        while super().get_param(super().pv.PARAM_TEMP)[1] != self.cs.temp * 100 and datetime.datetime.now() < temp_wait:
            continue
        # TODO Change time unit?
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=self.cs.time_shooting)
        while datetime.datetime.now() < end_time and self.shoot_on:
            super().take_picture(self.cs.binning, self.cs.exp, self.cs.path)
        self.signal_console.emit("Shooting Finished.", 1)
        self.standby()

    def stop(self):
        self.shoot_on = False
