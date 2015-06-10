__author__ = 'Amit'

import urllib2
import Quandl

def get_data():
    # Construct the Yahoo URL with the correct integer query parameters
    # for start and end dates. Note that some parameters are zero-based!
    ticker = 'GOOG/BOM_532155'
    quandl_url = "https://www.quandl.com/api/v1/datasets/%s.csv?auth_token=QydL2yFm-kAxpegBtht9" % (ticker,)

    # Try connecting to Yahoo Finance and obtaining the data
    # On failure, print an error message.
    print quandl_url
    try:
        yf_data = urllib2.urlopen(quandl_url).readlines()  # Ignore the header
        prices = []
        print('Total Rows: ' + str(len(yf_data)))
        for y in yf_data:
            print y.strip()
    except Exception, e:
        print "Could not download Quandl data: %s" % e
        return []
    return prices


mydata = Quandl.get('FRED/GDP')
print mydata