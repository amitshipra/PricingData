__author__ = 'dias'

import glob

CUR_DIR = "."

p = glob.glob("../exchanges-data/NASDAQ*")

with open(p[0]) as symbols:
    for symbol in symbols.readlines():
        print(symbol)