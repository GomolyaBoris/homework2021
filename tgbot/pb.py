import re
import requests
import json
# это ссылка ПриватБанка, который предоставляет курсы валют бесплатно в формате json.
# Единственная проблема в том, что это украинский банк и курс будет показываться через гривни.

URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

# загружает курсы валют по указанному URL-адресу и возвращает их в формате словаря.
def load_exchange():
    return json.loads(requests.get(URL).text)

# возвращает курсы валют по запрошенной валюте
def get_exchange(ccy_key):
    for exc in load_exchange():
        if ccy_key == exc['ccy']:
            return exc
    return False

# возвращает список валют в соответствии с шаблоном
def get_exchanges(ccy_pattern):
    result = []
    ccy_pattern = re.escape(ccy_pattern) + '.*'


    for exc in load_exchange():
        if re.match(ccy_pattern, exc['ccy'], re.IGNORECASE) is not None:
            result.append(exc)
        return result

