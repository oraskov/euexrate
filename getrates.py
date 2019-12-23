#! Python3
"""Script for grabbing exchange rates from net.

Use this script to web scrap data from https://www.ecb.europa.eu
for following (implemented) currencies: CAD, CHF, DKK, GBP, NOK, SEK, USD.
the table name in example is >>eurates<<
"""


from urllib.request import urlopen
import re
import datetime
import pandas
from bs4 import BeautifulSoup
import pymysql.cursors


__author__ = "Oliver Raskov"
__copyright__ = "Copyright 2018"
__credits__ = ["My family"]
__license__ = "GPL"
__version__ = "0.3"
__maintainer__ = "Oliver Raskov"
__email__ = "oliver.raskov@gmail.com"
__status__ = "Deployment"


def soup_creator(data):
    """ Creates the soup of soups. """
    mres = []
    for dat in data:
        mres.append(BeautifulSoup(dat, 'html.parser'))
    return mres


def latest(data):
    """ Extracts only the latest data. """
    words = re.split(r'\W+', data[1])
    currency = words[2]
    the_date = words[5] + '-' + words[6] + '-' + words[7]
    if datetime.date.fromordinal(
        datetime.date.today().toordinal()-1
    ) != the_date:
        the_date = str(
            datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        )
    the_rate = 1 / float(words[0] + '.' + words[1])
    return [currency, the_date, the_rate]


def extract_data(soups):
    """ Extract the wanted data from soups. """
    res = []
    for soup in soups:
        mres = []
        for content in soup.findAll('title'):
            for cont in content:
                mres.append(cont)
        res.append(latest(mres))
    return res


def insertion(cur, dat, val):
    """ Connector for MySQL. """
    con = pymysql.connect(
        host='localhost',
        user='someuser',
        password='somepass',
        db='somedb',
        charset='latin1',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with con.cursor() as cursor:
            sql = "INSERT INTO `eurates` (`currency`, `date`, `multiplier`) \
                 VALUES ('{}', '{} 06:00:00', {})".format(cur, dat, val)
            cursor.execute(sql)
        con.commit()
    finally:
        con.close()


def main():
    """ The magic starts here. """


if __name__ == "__main__":
    main()
