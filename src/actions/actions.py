"""

Author: Fernando Ferrari

Created on: ...

This file contains a class with the methods to execute all of the program's possible actions;
in other words, this is the program's main controller.

Said class requires methods from the PIXIS driver class in src/driver/pixis.py and
the camera.ini settings class on src/saving/camera_settings.py

"""

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
                    self.shooter.standby()
                    self.gain_to_driver()
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
                self.shooter.standby()
                self.shooter.shoot_on = False
                self.driver.close()
                if not self.driver.error():
                    self.console.write_to_console("Disconnected Successfully.", 1)
                    self.is_connected = False
                else:
                    self.console.write_to_console("Failed to Disconnect. PVCAM Error.", 3)
            except Exception as e:
                self.console.write_to_console("Connection Error: " + str(e), 3)

    def get_temp(self):
        if not self.shooter.shoot_on:
            return self.driver.get_param(self.driver.pv.PARAM_TEMP)[1]
        else:
            self.console.write_to_console("Unavailable during acquisition.", 2)

    def shoot(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        else:
            self.shooter.start()

    def stop(self):
        if not self.is_connected:
            self.console.write_to_console("Not Connected.", 2)
        elif not self.shooter.shoot_on:
            self.console.write_to_console("Already Stopped.", 2)
        else:
            self.console.write_to_console("Stopping...", 0)
            self.shooter.shoot_on = False
            self.console.write_to_console("Stopped successfully", 1)
            # self.shooter.standby()

    def gain_to_driver(self):
        if self.driver.pvcam:
            self.cs.load_settings()
            self.driver.set_param(self.driver.pv.PARAM_GAIN_INDEX, int(self.cs.gain) + 1)
