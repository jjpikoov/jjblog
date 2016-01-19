import calendar


class Notification():
    """
    Notification class for announcing results of some operations.
    """
    def __init__(
            self, active=False, title=None, description=None, color=None):
        """
        Constructor for changing defaults values (False or None).
        """
        self.active = active
        self.title = title
        self.description = description
        self.color = color


def validate_date(day, month, year):
    """
    Function checks if date given by user is proper one.
    """
    if month == 2:
        if calendar.isleap(year):
            if day > 29:
                return False
        else:
            if day > 28:
                return False
    return True
