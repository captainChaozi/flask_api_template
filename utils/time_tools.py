import calendar
import datetime


def current_month():
    today = datetime.date.today()
    year = today.year
    month = today.month
    start = calendar.monthrange(year, month)[0]
    end = calendar.monthrange(year, month)[-1]
    start = datetime.date(year, month, start)
    end = datetime.date(year, month, end)
    return start, end
