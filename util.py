import datetime


class Notification():
    def __init__(
            self, active=False, title=None, description=None, color=None):
        self.active = active
        self.title = title
        self.description = description
        self.color = color


def validate_date(day, month, year):
    try:
        datetime.datetime(int(year), int(month), int(day))
    except:
        return False
    return True
