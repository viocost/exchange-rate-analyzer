#!/bin/env python
#
from bs4 import BeautifulSoup
import requests
import datetime
import sqlite3


def main():
    with sqlite3.connect('/home/kostia/projects/banks/data.db') as con:
        cur = con.cursor()
        cur.execute(
            '''
                CREATE TABLE IF NOT EXISTS exchange_rate (
                    date text,
                    bank text,
                    buy real,
                    sell real
                )
            '''
            )


        timestamp = str(datetime.datetime.now().isoformat())

        r = requests.get('https://mainfin.ru/currency/usd/ekaterinburg?sort=-buy_course_1')

        soup = BeautifulSoup(r.text, 'html.parser')

        table = list(filter(lambda x: "hidden-info-block" not in str(x), soup.select('#g_bank_rates > table > tbody > tr')))

        for row in table:
            cells = list(row.children)
            cur.execute(f'''
                INSERT INTO exchange_rate (date, bank, buy, sell) values (
                    "{timestamp}",
                    "{cells[0].get_text()}",
                    "{cells[1].get_text()}",
                    "{cells[2].get_text()}"
                )
            ''')
if __name__ == '__main__':
    main()
