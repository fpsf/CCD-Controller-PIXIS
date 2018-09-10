import datetime

from driver.pixis import CCDPixis


class Actions(CCDPixis):

    def __init__(self):
        super().__init__()
        self.shoot_on = True

    def standby(self):
        super().set_param(super().pv.PARAM_TEMP_SETPOINT, 2500)

    def shoot(self, set_temp, shoot_time, b, exp, path):
        super().set_param(super().pv.PARAM_TEMP_SETPOINT, set_temp)
        while super().get_param(super().pv.PARAM_TEMP)[1] != set_temp * 100:
            continue
        # TODO Change time unit?
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=shoot_time)
        while datetime.datetime.now() < end_time:
            super().take_picture(b, exp, path)
