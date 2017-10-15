import datetime as dt

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
dateVal = dt.datetime.now() - dt.timedelta(hours = 4)


def get_date(retType):
    if(retType):
        d = str(dateVal)
        return (months[int(d[5:7]) - 1] + " " + d[8:10] + ", " + d[0:4])
    else:
        return dateVal.strftime('%Y-%m-%d')

def getDate():
    return "The date today is " + str(get_date(True)) + "."

def get_time():
    if (int(dateVal.strftime('%H')) < 12):
        return str(dateVal.strftime('%H:%M')) + " AM"
    else:
        return str(int(dateVal.strftime('%H')) % 12) + str(dateVal.strftime(':%M')) + " PM"

def getTime():
    return "The time is " + str(get_time()) + "."