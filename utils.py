import datetime
import time

def timestamp(t=None, fmt='%Y%m%d_%H%M%S'):
    if t is None:
        t = time.localtime()
    return time.strftime(fmt, t)

def weekday(t=None):
    if t is None:
        t = datetime.date.today()
    d = datetime.date.weekday(t)
    if 6 == d:
        res = '日'
    else:
        res = str(d + 1)
    return res