# HELPER FUNCTIONS
import datetime
import uuid


def is_logged_in():
    pass


def current_date():
    x = datetime.datetime.now()
    return (str(x.year) + '-' + str(x.strftime("%m")) + '-' + str(x.strftime("%d")))


# def generate_uuid():
#     pass
