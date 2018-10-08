import datetime
import time

from PyQt5 import QtCore

from actions.console import ConsoleThreadOutput
from driver.pixis import CCDPixis
from saving.camera_settings import CameraSettings


class Shooter(QtCore.QThread):

    def __init__(self):
        super().__init__()
        self.driver = CCDPixis()
        self.cs = CameraSettings()
        self.shoot_on = None
        self.console = ConsoleThreadOutput()

    def standby(self):
        try:
            self.console.write_to_console("Entering Standby Mode...", 1)
            self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, 2500)
            # self.signal_console.emit("Success", 1)
        except Exception as e:
            self.console.write_to_console("Standby Failed: " + str(e), 3)

    def run(self):
        try:

            # ########################################## Preparations: ##############################################

            self.console.write_to_console("Preparing Acquisition...", 0)
            time.sleep(1)
            self.shoot_on = True
            self.driver.set_param(self.driver.pv.PARAM_TEMP_SETPOINT, int(self.cs.temp) * 100)
            temp_wait = datetime.datetime.now() + datetime.timedelta(seconds=600)
            self.console.write_to_console("Waiting for Camera Temperature to be " + str(self.cs.temp), 0)
            time.sleep(1)
            while (self.driver.get_param(self.driver.pv.PARAM_TEMP)[1] != int(self.cs.temp) * 100 and
                   datetime.datetime.now() < temp_wait) and self.shoot_on:
                # self.console.write_to_console(str(self.driver.get_param(self.driver.pv.PARAM_TEMP)[1] / 100), 0)
                # time.sleep(1)
                continue
            # TODO Change time unit?
            if self.shoot_on:
                self.console.write_to_console("Initiating Acquisition...", 0)
                time.sleep(1)
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=int(self.cs.time_shooting))
            pic_counter = 1

            # ########################################## Preparations ##############################################

            while datetime.datetime.now() < end_time and self.shoot_on:
                self.driver.take_picture(int(self.cs.binning), int(self.cs.exp), self.cs.path)
                if not self.driver.error():
                    self.console.write_to_console("\n", 1)
                    self.console.write_to_console("Image nº: " + str(pic_counter) + "Acquired.", 1)
                    self.console.write_to_console("Time Remaining:" + str(end_time - datetime.datetime.now()), 1)
                    self.console.write_to_console("Current Temperature: " +
                                                  "{0:.2f}".format(self.get_temp() / 100, 0), 1)
                    self.console.write_to_console("Waiting " + str(self.cs.acq_wait) + "For Next Image...", 1)
                    time.sleep(int(self.cs.acq_wait))
                    pic_counter += 1
                else:
                    self.console.write_to_console("\n", 1)
                    self.console.write_to_console("Shooting Failed: PVCAM Error", 3)
                    self.console.write_to_console("Aborting...", 3)
                    self.shoot_on = False
            self.console.write_to_console("Shooting Finished.", 1)
            self.standby()

        except Exception as e:
            self.console.write_to_console("Shooting Failed: " + str(e), 3)
