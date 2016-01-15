import calendar


class Notification():
    def __init__(
            self, active=False, title=None, description=None, color=None):
        self.active = active
        self.title = title
        self.description = description
        self.color = color


def validate_date(day, month, year):
    if month == 2:
        if calendar.isleap(year):
            if day > 29:
                return False
        else:
            if day > 28:
                return False
    return True
