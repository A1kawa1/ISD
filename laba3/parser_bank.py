import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


url = 'https://moskva.vbr.ru/banki/kurs-valut/'


@dataclass
class Bank:
    name: str
    buy: float
    sell: float


def get_data_bank(count=5):
    try:
        result = []
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'lxml')
        all_bank = bs.find_all(
            'tr', attrs={'class': 'rates-table-expand with-offices'})[:count]
        for bank in all_bank:
            bank = Bank(
                name=bank.find(
                    'span', attrs={'class': 'rates-name-bank'}).text.strip(),
                buy=float(bank.find_all(
                    'div', attrs={'class': 'rates-calc-block'})[0].text.strip()[:-2].replace(',', '.')),
                sell=float(bank.find_all(
                    'div', attrs={'class': 'rates-calc-block'})[1].text.strip()[:-2].replace(',', '.'))
            )
            result.append(bank)
        return result
    except Exception as e:
        return None
