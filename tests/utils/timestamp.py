from datetime import datetime

def getTimestampStr(year = None, month = None, day = None, hour = None, minute = None, second = None):
    """ Returns the timestamp string compatible for the server """
    instant = None
    if not [x for x in (year, month, day, hour, minute, second) if x is None]:
        instant = datetime(year,month,day,hour,minute, second)
    else:
        instant = datetime.utcnow()
    return datetime.strftime(instant, '%Y-%m-%dT%H:%M:%SZ')
