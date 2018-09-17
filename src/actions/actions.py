"""

Author: Fernando Ferrari

Created on: ...

This file contains a class with the methods to execute all of the program's possible actions;
in other words, this is the program's main controller.

Said class requires methods from the PIXIS driver class in src/driver/pixis.py and
the camera settings class on src/saving/camera_settings.py

"""

import datetime

from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Actions(CCDPixis):

    def __init__(self):
        super().__init__()
        self.cs = CameraSettings()
        self.shoot_on = None

    def connect(self):
        super().open()

    def disconnect(self):
        super().close()

    def standby(self):
        super().set_param(super().pv.PARAM_TEMP_SETPOINT, 2500)

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

    def stop(self):
        self.shoot_on = False
