__author__ = 'Amit'

import datetime
import lxml.html
import urllib2


def obtain_parse_wiki_snp500():
    """Download and parse the Wikipedia list of S&P500
    constituents using requests and libxml.

    Returns a list of tuples for to add to MySQL."""

    # Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    # Use libxml to download the list of S&P500 companies and obtain the symbol table
    page = lxml.html.parse('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    symbolslist = page.xpath('//table[1]/tr')[1:]

    # Obtain the symbol information for each row in the S&P500 constituent table
    symbols = []
    for symbol in symbolslist:
        tds = symbol.getchildren()
        sd = {'ticker': tds[0].getchildren()[0].text,
              'name': tds[1].getchildren()[0].text,
              'sector': tds[3].text}
        print(sd)
        # Create a tuple (for the DB format) and append to the grand list
        symbols.append((sd['ticker'], 'stock', sd['name'],
                        sd['sector'], 'USD', now, now))
    return symbols


def get_daily_historic_data_yahoo(ticker,
                                  start_date=(2000, 1, 1),
                                  end_date=datetime.date.today().timetuple()[0:3]):
    """Obtains data from Yahoo Finance returns and a list of tuples.

  ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
  start_date: Start date in (YYYY, M, D) format
  end_date: End date in (YYYY, M, D) format"""

    # Construct the Yahoo URL with the correct integer query parameters
    # for start and end dates. Note that some parameters are zero-based!
    yahoo_url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % \
                (ticker, start_date[1] - 1, start_date[2], start_date[0], end_date[1] - 1, end_date[2], end_date[0])

    # Try connecting to Yahoo Finance and obtaining the data
    # On failure, print an error message.
    try:
        yf_data = urllib2.urlopen(yahoo_url).readlines()[1:]  # Ignore the header
        prices = []
        for y in yf_data:
            p = y.strip().split(',')
            prices.append((datetime.datetime.strptime(p[0], '%Y-%m-%d'),
                           p[1], p[2], p[3], p[4], p[5], p[6]))
    except Exception, e:
        print "Could not download Yahoo data: %s" % e
    return prices


prices = get_daily_historic_data_yahoo('BCOR')

for price in prices:
    print(price)
print 'Total Rows: ', len(prices)
