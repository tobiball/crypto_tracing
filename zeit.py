import calendar
import datetime

from pytz import timezone


class Timing:
    def __init__(self):
        self.current_datetime = datetime.datetime.now()

    def spx_trading_hours(self):
        est = timezone('US/Eastern')
        est_datetime = self.current_datetime.astimezone(est)
        est_weekday = calendar.weekday(est_datetime.year, est_datetime.month, est_datetime.day)

        if (est_weekday < 4 or
                est_weekday == 4 and est_datetime.hour * 60 + est_datetime.minute < 960 or
                est_weekday == 6 and est_datetime.hour * 60 + est_datetime.minute > 1020):
            return True
        else:
            return False
