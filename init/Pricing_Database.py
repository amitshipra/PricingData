__author__ = 'dias'

import psycopg2 as PG
import psycopg2.extras

# Move it to script parameters.
DATABASE_NAME = "EquityPrices2"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "dias"


DATABASE_URL = "dbname={0} user={1} password={2}".format(DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)


def get_connection():
    conn = PG.connect(DATABASE_URL)

    if conn is None:
        raise RuntimeError('Connection could not established')

    print('Connection Established')
    return conn

def get_dict_cursor():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if cur is None:
        raise RuntimeError('Could not get Dict Cursor')

    return cur


