from typing import Dict, List

from bs4 import BeautifulSoup

from sess import sess
from config import URL

from model import Model


def prepare_url_with_prices(raw_url: str) -> str:
    return URL + raw_url.replace('/instrukciya', '').replace('?m=1', '') + '/ceni'


def get_price_page_source(url: str):
    return sess.get(url)


def get_price_info(data: Dict) -> List:
    url_price = prepare_url_with_prices(data['url'])
    html = get_price_page_source(url_price)
    soup = BeautifulSoup(html, 'lxml')
    stores = [el.text for el in soup.find_all(class_='ama-org-name')]
    prices = [float(el.text.split('р')[0].replace('\xa0', ''))
                for el in soup.find_all(class_='ama-org-minp')]
    ids = [data['id'] for _ in range(len(stores))]
    names = [data['name'] for _ in range(len(stores))]
    return list(zip(ids, names, stores, prices))


def save_prices_to_db(data: Dict) -> None:
    prices = get_price_info(data)
    model = Model()
    model.insert('prices', ['drug_id', 'drug_name', 'store_name', 'price'], prices)


