# HELPER FUNCTIONS
import datetime

def is_logged_in():
    pass

def current_date():
    x = datetime.datetime.now()
    return (str(x.year) + '-' + str(x.strftime("%m")) + '-' + str(x.strftime("%d")))