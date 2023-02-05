import requests
import json
from config import currencies

class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount):
        if quote == base:
            raise ConvertionException('Выберите разные валюты')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[currencies[base]]) * int(amount)

        return total_base