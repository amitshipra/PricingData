__author__ = 'Amit'

import Quandl

MY_API_KEY = 'QydL2yFm-kAxpegBtht9'


def get_data(q_code):
    prices = Quandl.get(q_code)
    return prices


print(get_data("FRED/GDP"))
