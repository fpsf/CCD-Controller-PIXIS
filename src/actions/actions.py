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

from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Actions(QtCore.QObject):

    signal_console = QtCore.pyqtSignal(name="signalConsole")

    def __init__(self):
        super(Actions, self).__init__()
        self.driver = CCDPixis()
        # self.driver.__init__()
        self.cs = CameraSettings()
        self.shoot_on = None
        self.is_connected = False

    def connect(self):
        if self.is_connected:
            self.signal_console.emit("Already Connected.", 2)
        else:
            self.signal_console.emit("Connecting...", 2)
            self.driver.open()
            if not self.driver._error():
                self.signal_console.emit("Connected Successfully.", 1)
                self.is_connected = True
            else:
                self.signal_console.emit("Connection Error...", 3)

    def disconnect(self):
        if not self.is_connected:
            self.signal_console.emit("Not Connected.", 2)
        else:
            self.signal_console.emit("Disconnecting...", 2)
            self.driver.close()
            if not self.driver._error():
                self.signal_console.emit("Disconnected Successfully.", 1)
            else:
                self.signal_console.emit("Connection Error...", 3)

    def standby(self):
        self.signal_console.emit("Entering Standby Mode...", 1)
        self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, 2500)
        # self.signal_console.emit("Success", 1)

    def get_temp(self):
        return self.driver.get_param(self.driver.pv.PARAM_TEMP)[1]

    def shoot(self):
        self.shoot_on = True
        self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, int(self.cs.temp) * 100)
        temp_wait = datetime.datetime.now() + datetime.timedelta(seconds=600)
        while self.driver.get_param(self.driver.pv.PARAM_TEMP)[1] != int(self.cs.temp) * 100 and datetime.datetime.now() < temp_wait:
            continue
        # TODO Change time unit?
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=int(self.cs.time_shooting))
        while datetime.datetime.now() < end_time and self.shoot_on:
            self.driver.take_picture(int(self.cs.binning), int(self.cs.exp), self.cs.path)
        self.signal_console.emit("Shooting Finished.", 1)
        self.standby()

    def stop(self):
        self.shoot_on = False
