#!/bin/env python
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


def filter_dates(dates):
    return filter(lambda x: datetime.fromisoformat(x[0]).time().hour in range(11, 19), dates)

class Bank:
    def __init__(self, data):
        self.name = data[0]
        self.buy = data[1]
        self.sell = data[2]
        self.diff = self.sell - self.buy

    def __str__(self):
        return f"{self.name}:  Buy: {self.buy} | Sell: {self.sell}"


class Sample:
    def __init__(self, date, rows):
        self.date = date
        self._banks = []
        for row in rows:
            self.add(Bank(row))

    def add(self, bank):
        self._banks.append(bank)

    def sell(self):
        return sorted(self._banks, key=lambda b: b.sell)

    def buy(self):
        return sorted(self._banks, key=lambda b: b.buy * -1)

    def diff(self):
        return sorted(self._banks, key=lambda b: (b.sell - b.buy))

    def __contains__(self, bank_name: str):
        for bank in self._banks:
            if bank.name == bank_name:
                return True
        return False

    def get_bank(self, bank_name):
        for bank in self._banks:
            if bank.name == bank_name:
                return bank
        return Bank([bank_name, 0, 0])

    def print(self, mode="sell"):
        print(f'SAMPLE {self.date} mode: {mode}')
        for bank in eval(f'self.{mode}()'):
            print(bank)
        print("\n\n")




class Samples:
    def __init__(self):
        self.samples = []

    def add(self, sample):
        self.samples.append(sample)

    def get_bank_data(self, bank_name, mode='sell'):
        return [ eval(f'sample.get_bank("{bank_name}").{mode}') for sample in self.samples ]

def plot_banks(samples, banks, mode):
    titles = {
        "buy": "Buy: the greater - the better",
        "sell": "Sell: the lower - the better",
        "diff": "Diff: the lower - the better"
    }
    legends = []
    for bank in banks:
        plt.plot(samples.get_bank_data(bank, mode))
        legends.append(bank)
    plt.legend(legends)
    plt.title(titles[mode])
    plt.show()

def main():
    samples = Samples()
    with sqlite3.connect('/home/kostia/projects/banks/data.db') as con:
        cur = con.cursor()
        dates = filter_dates(cur.execute(
            '''
                SELECT DISTINCT date FROM exchange_rate;
            '''
            ))

        for date in dates:

            cur1 = con.cursor()

            select = list(cur1.execute(
                f'''
                SELECT bank, buy, sell FROM exchange_rate
                WHERE date="{date[0]}"
                ORDER BY buy DESC
                LIMIT 20
                '''
            ))

            sample = Sample(date, select)

            if "Ак Барс Банк" not in sample:
                continue

            samples.add(sample)

            sample.print('diff')

    banks = ["Ак Барс Банк", "БКС Банк", "Восточный Банк", "Россельхозбанк"]
    plot_banks(samples, banks, 'sell')


if __name__ == '__main__':
    main()
