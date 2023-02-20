import random
from time import sleep

from bs4 import BeautifulSoup

from db import insert, clear_table
from config import URL, PAGES
from sess import sess, get_page_source


def get_urls_names_from_page(html: str, is_first = False):
    soup = BeautifulSoup(html, 'lxml')
    if is_first:
        elements = soup.find_all(class_='ama-found-product')
        return [(el.get('href').replace(URL, ''),
                 el.find(class_='ama-found-product-name').text)
                for el in elements]
    return [(el.get('href').replace(URL, ''),
             el.text)
            for el in soup.find_all(class_='product-name')]


def collect_all_urls(pages_count: int) -> None:
    clear_table('urls')
    for page in range(1, pages_count):
        html = get_page_source(URL, params={'page': page})
        flag = True if page == 1 else False
        data = get_urls_names_from_page(html, is_first=flag)
        print(data)
        insert('urls', ['url', 'name'], data)
        sleep(random.uniform(0,2))


def test_get_url():
    html = get_page_source(URL, params={'page': 2})
    # print(html)
    print(get_urls_names_from_page(html))


if __name__ == "__main__":
    collect_all_urls(4)