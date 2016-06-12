import datetime

def get_today_string():
    today = datetime.date.today()
    today = today.strftime("%d-%m-%Y")
    return today