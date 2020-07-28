import datetime

def Today():
    return datetime.date.today()

def OneDay():
    return datetime.timedelta(days=1)

def Yesterday():
    return Today()-OneDay()

def DateToStr(date):
    return date.strftime('%Y-%m-%d')

def StrToDate(dateStr):
    try:
        return datetime.datetime.strptime(dateStr,'%Y-%m-%d')
    except :
        return None