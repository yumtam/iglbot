import settings as s
from datetime import timezone, timedelta, datetime

def gettime(delta=0):
    tz = timezone(timedelta(hours=s.TIMEZONE))
    dt = datetime.now().astimezone(tz)
    dt += timedelta(seconds=delta)
    return f'{dt:%H:%M:%S}'
