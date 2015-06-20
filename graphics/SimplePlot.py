__author__ = 'dias'

import init.Pricing_Database as db
import matplotlib.pyplot as plot

GET_PRICES_BY_SYMBOLID_QUERY = """
            select dp.price_date, dp.open_price as open,
            dp.close_price as close, dp.low_price as low,
            dp.high_price high
            from daily_price dp
            where dp.symbol_id=%s
            order by price_date
        """


def display_chart(symbol_id):
    print('Displaying chart for symbol_id')
    with db.get_dict_cursor() as cur:
        cur.execute(GET_PRICES_BY_SYMBOLID_QUERY, (symbol_id,))
        prices = cur.fetchall()
        data = list()
        for price in prices:
            print('Date [{0}]  OPEN [{1}]  HIGH [{2}]  LOW [{3}] CLOSE [{4}]'.format(price['price_date'], price['open'],
                                                                                     price['high'], price['low'],
                                                                                     price['close']))
            data.append((price['open'], price['close'], price['high'], price['low']))

        print('Data loaded. Plotting...')
        plot.xlabel('Date')
        plot.ylabel('Price')
        plot.plot(data)
        plot.savefig('myfilename.png')

display_chart(456)
