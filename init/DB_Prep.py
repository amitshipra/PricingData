__author__ = 'Amit'

import psycopg2 as PG
import datetime
import urllib2

# Move it to script parameters.
DATABASE_NAME = "EquityPrices"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "postgres"
EXCHANGE_DATA_DIR = "..\\exchanges-data\\"

DATABASE_URL = "dbname={0} user={1} password={2}".format(DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)

DATA_VENDOR = "Yahoo Finance"


def get_symbols(exchange):
    print("Loading symbols for {0}".format(exchange))
    symbols = list()
    with open(EXCHANGE_DATA_DIR + exchange + '-tickers') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('Symbol'):
                continue
            sep_index = -1
            for idx, ch in enumerate(line):
                if ch == '' or ch == '\t':
                    sep_index = idx

            symbol = line[:sep_index]
            description = line[sep_index:]
            #            print("Symbol [{0}] Description [{1}]".format(symbol, description))
            symbols.append((symbol, description))
    return symbols


def load_data():
    conn = PG.connect(DATABASE_URL)

    # Test Connection
    if conn is None:
        print('Connection could not be established')
    else:
        print('Connection Established')

    with conn.cursor() as cur:
        # Create Tables.
        cur.execute("""
                DROP TABLE IF EXISTS exchange CASCADE;
                CREATE TABLE exchange (
                  id serial PRIMARY KEY ,
                  abbrev text NOT NULL,
                  exchange_name text NOT NULL,
                  city text NULL,
                  country text NULL,
                  currency text NULL,
                  timezone_offset time NULL,
                  created_date timestamp NOT NULL DEFAULT now(),
                  last_updated_date timestamp NOT NULL DEFAULT now()
                );
                INSERT INTO exchange(abbrev,exchange_name,city,country,currency) VALUES('NASDAQ','National Association of Securities Dealers Automated Quotations Exchange','NY','US','USD');
                INSERT INTO exchange(abbrev,exchange_name,city,country,currency) VALUES('NYSE','New York Stock Exchange','NY','US','USD');
                INSERT INTO exchange(abbrev,exchange_name,city,country,currency) VALUES('TSX','Toronto Stock Exchange','TO','CA','CAD');
        """)
        cur.execute('commit;')
        print('Exchange table created. Data inserted')

        cur.execute("""
                DROP TABLE IF EXISTS data_vendor CASCADE;
                CREATE TABLE data_vendor (
                  id serial PRIMARY KEY,
                  vendor_name text NOT NULL,
                  website_url text NULL,
                  support_email text NULL,
                  created_date timestamp NOT NULL DEFAULT now(),
                  last_updated_date timestamp NOT NULL DEFAULT now()
                );

                INSERT INTO data_vendor(vendor_name,website_url,support_email) VALUES('Google Finance','www.google.com/finance',NULL);
                INSERT INTO data_vendor(vendor_name,website_url,support_email) VALUES('Yahoo Finance','www.yahoo.com/finance',NULL);
                INSERT INTO data_vendor(vendor_name,website_url,support_email) VALUES('Interactive Data','www.interactivedata.com','support@interactivedata.com');
        """)
        cur.execute('commit;')
        print('Data Vendor table created. Data inserted')

        cur.execute("""
                DROP TABLE IF EXISTS symbol CASCADE;
                CREATE TABLE symbol (
                  id serial PRIMARY KEY,
                  exchange_id int NOT NULL REFERENCES exchange(id),
                  ticker text NOT NULL,
                  instrument text NOT NULL DEFAULT 'EQUITY',
                  description text NOT NULL,
                  sector text NULL,
                  currency text NULL,
                  created_date timestamp NOT NULL DEFAULT now(),
                  last_updated_date timestamp NOT NULL DEFAULT now()
                );
        """)

        cur.execute('commit;')
        print('Table Symbol created. Inserting data')

        # Post the Exchanges and Data Vendors inserts. Now insert symbols based on Exchanges.
        cur.execute("select * from exchange")
        exchanges = cur.fetchall()
        for exchange in exchanges:
            abbrev = exchange[1]
            exchange_id = exchange[0]
            print("Working for Exchange [{0}]".format(abbrev))
            symbols = get_symbols(abbrev)
            print("Total Symbols for [{0}] are [{1}]".format(abbrev, len(symbols)))
            for symbol, description in symbols:
                cur.execute("INSERT INTO symbol(exchange_id, ticker, instrument, description) VALUES (%s,%s,%s,%s)",
                            (exchange_id, symbol, 'EQUITY', description))
            cur.execute('commit;')
            print("Symbols [{0}] loaded in database for {1}".format(len(symbols), abbrev))

        cur.execute("""
                DROP TABLE IF EXISTS daily_price CASCADE;
                CREATE TABLE daily_price (
                  id serial PRIMARY KEY,
                  data_vendor_id int NOT NULL REFERENCES data_vendor(id),
                  symbol_id int NOT NULL REFERENCES symbol(id),
                  price_date date NOT NULL,
                  open_price numeric NOT NULL,
                  high_price numeric NOT NULL,
                  low_price numeric NOT NULL,
                  close_price numeric NOT NULL,
                  created_date timestamp NOT NULL DEFAULT now(),
                  last_updated_date timestamp NOT NULL DEFAULT now()
                );
        """)

        cur.execute('commit;')
        print('Table Daily_Price created. Inserting data. This will take time.')

        cur.execute("select id from data_vendor where vendor_name=%s", (DATA_VENDOR,))
        vendor_id = cur.fetchone()[0]
        print "Vendor Id {0}".format(vendor_id)

        for exchange in exchanges:
            abbrev = exchange[1]
            exchange_id = exchange[0]
            print("Loading prices for Exchange [{0}]".format(abbrev))
            cur.execute("select id, ticker from symbol where exchange_id=%s", (exchange_id,))
            symbols = cur.fetchall()
            for sym_id, symbol in symbols:
                prices = get_daily_historic_data_yahoo(symbol)
                total_prices = len(prices)
                if total_prices == 0:
                    print("Could not load prices for Symbol [{0}] for Exchange [{1}]".format(symbol, abbrev))
                    continue
                else:
                    print(
                    "Loading [{0}] prices for Symbol [{1}] for Exchange [{2}]".format(total_prices, symbol, abbrev))

                for price in prices:
                    price_date = price[0].date()
                    cur.execute(
                        "INSERT INTO daily_price(data_vendor_id, symbol_id, price_date, open_price, high_price, low_price, close_price) values(%s,%s,%s,%s,%s,%s,%s)",
                        (vendor_id, sym_id, price_date, price[1], price[2], price[3], price[4]))
                cur.execute('commit;')


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
        return []
    return prices


load_data()
