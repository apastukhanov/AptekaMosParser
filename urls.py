from bs4 import BeautifulSoup

from db import insert
from config import URL, PAGES
from sess import sess


def get_page_source(page_num: int) -> str:
    params = {'page': page_num}
    return sess.get(URL, params=params).text


def get_urls_names_from_page(html: str):
    soup = BeautifulSoup(html, 'lxml')
    elements = soup.find_all(class_='ama-found-product')
    return [(el.get('href').replace(URL, ''),
             el.find(class_='ama-found-product-name').text)
            for el in elements]


def collect_all_urls() -> None:
    for page in range(PAGES):
        html = get_page_source(page)
        data = get_page_source(html)
        insert('urls', ['url', 'name'], data)

