import datetime
import time

from PyQt5 import QtCore

from actions.console import ConsoleThreadOutput
from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Shooter(QtCore.QThread):

    taking_picture = QtCore.pyqtSignal()
    shooting_failure = QtCore.pyqtSignal()
    pvcam_failure = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.end_time = None
        self.pic_counter = 1
        self.driver = CCDPixis()
        self.cs = CameraSettings()
        self.shoot_on = None
        self.console = ConsoleThreadOutput()

    def run(self):
        try:

            # ########################################## Preparations: ##############################################

            self.cs.load_settings()
            self.shoot_on = True
            self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, int(self.cs.temp) * 100)
            temp_wait = datetime.datetime.now() + datetime.timedelta(seconds=600)
            # self.console.write_to_console("Waiting for Camera Temperature to be " + str(self.cs.temp), 0)
            while (self.driver.get_param(self.driver.pv.PARAM_TEMP)[1] > int(self.cs.temp) * 100 and
                   datetime.datetime.now() < temp_wait) and self.shoot_on:
                continue
            # TODO Change time unit?

            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(seconds=int(self.cs.time_shooting))
            self.end_time = end_time

            # ########################################## Preparations ##############################################

            while datetime.datetime.now() < end_time and self.shoot_on:
                self.taking_picture.emit()
                self.driver.take_picture(int(self.cs.binning), float(self.cs.exp), self.cs.path)
                if not self.driver.error():
                    print("\n")
                    print("Picture: " + str(self.pic_counter))
                    print("\n")
                    time.sleep(int(self.cs.acq_wait))
                    self.pic_counter += 1
                else:
                    self.pvcam_failure.emit()
            self.pic_counter = 1

        except Exception:
            self.shooting_failure.emit()
