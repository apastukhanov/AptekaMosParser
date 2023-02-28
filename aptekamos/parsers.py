from abc import ABC, abstractmethod
from functools import partial
import itertools
import random
from random import choice

from multiprocessing import Pool

from time import sleep
from typing import Protocol, Dict, List

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import HEADERS, URL
from model import Model


def make_prices_page_url(raw_url: str) -> str:
    return URL + raw_url.replace('/instrukciya', '').replace('?m=1', '') + '/ceni'


class Parser(ABC):
    @abstractmethod
    def get_urls_from_page(self):
        ...

    @abstractmethod
    def get_prices(self):
        ...

    @abstractmethod
    def collect_all_urls(self):
        ...

    def collect_all_prices(self, model: Model):
        output = []
        model.clear_table('prices')
        list_data = model.fetchall('urls', ['id', 'url', 'name'])
        for data in list_data:
            prices = self.get_prices(data)
            output.append(prices)
            model.insert('prices', ['drug_id', 'drug_name', 'store_name', 'price'], prices)
        return output


class BasicParser(Parser):
    def __init__(self, user_agents: List[str] = None,
                 proxies: List[str] = None):
        self.sess = requests.Session()
        self.sess.headers.update(HEADERS)
        self.user_agents = user_agents
        self.proxies = proxies

    def get_urls_from_page(self, html: str, is_first: bool):
        soup = BeautifulSoup(html, 'lxml')
        if is_first:
            elements = soup.find_all(class_='ama-found-product')
            return [(el.get('href').replace(URL, ''),
                     el.find(class_='ama-found-product-name').text)
                    for el in elements]
        return [(el.get('href').replace(URL, ''),
                 el.text)
                for el in soup.find_all(class_='product-name')]

    def get_prices(self, data: Dict):
        url_price = make_prices_page_url(data['url'])
        html = self.get_page_source(url_price)
        return self.parse_drugs_prices(html, data)

    def parse_drugs_prices(self, html: str, data: Dict):
        soup = BeautifulSoup(html, 'lxml')
        stores = [el.text for el in soup.find_all(class_='ama-org-name')]
        prices = [float(el.text.split('р')[0].replace('\xa0', ''))
                  for el in soup.find_all(class_='ama-org-minp')]
        ids = [data['id'] for _ in range(len(stores))]
        names = [data['name'] for _ in range(len(stores))]
        return list(zip(ids, names, stores, prices))


    def _helper_url_collector(self, page: int):
        html = self.get_page_source(URL, params={'page': page})
        flag = True if page == 1 else False
        data = self.get_urls_from_page(html, is_first=flag)
        sleep(random.uniform(0, 1.2))
        return data

    def collect_all_urls(self, pages_count: int, model: Model):
        model.clear_table('urls')
        output = []
        for page in range(1, pages_count):
            data = self._helper_url_collector(page)
            model.insert('urls', ['url', 'name'], data)
            output.append(data)
        return list(itertools.chain.from_iterable(output))

    def get_page_source(self, url: str,
                        params: Dict = None):
        if self.user_agents:
            self.sess.headers['user-agent'] = choice(self.user_agents)
        req_fn = self.sess.get
        if params:
            req_fn = partial(self.sess.get, params=params)
        if self.proxies:
            proxy = choice(self.proxies)
            req_fn = partial(req_fn, proxies={'https': 'https://' + proxy})
        html = req_fn(url).text
        return html


class MultiStreamsParser(BasicParser):
    def __init__(self, streams_count: int,
                 user_agents: List[str] = None,
                 proxies: List[str] = None):
        super().__init__(user_agents, proxies)
        self.streams_count = streams_count

    def collect_all_urls(self, page_count: int, model: Model):
        model.clear_table('urls')
        with Pool(self.streams_count) as p:
            result = p.map(self._helper_url_collector, range(1, page_count))
        data = list(itertools.chain.from_iterable(result))
        model.insert('urls', ['url', 'name'], data)
        return data

    def collect_all_prices(self, model: Model):
        list_data = model.fetchall('urls', ['url', 'id', 'name'])
        model.clear_table('prices')
        with Pool(self.streams_count) as p:
            result = p.map(self.get_prices, list_data)
        data = list(itertools.chain.from_iterable(result))
        model.insert('prices', ['drug_id', 'drug_name', 'store_name', 'price'], data)
        return data


class WebBrowserParser(Parser):

    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)

    def get_urls_from_page(self):
        return [(el.get_property('href').replace(URL, ''),
                 el.get_property('innerText')) for el in
                self.driver.find_elements(by=By.CLASS_NAME,
                                          value='product-name')]

    def collect_all_urls(self, pages_count: int, model: Model):
        model.clear_table('urls')
        output = []
        for page in range(1, pages_count):
            self.driver.get(URL + f'/page={page}')
            data = self.get_urls_from_page()
            model.insert('urls', ['url', 'name'], data)
            output.append(data)
        return list(itertools.chain.from_iterable(output))

    def get_prices(self, data: Dict):
        url_price = make_prices_page_url(data['url'])
        self.driver.get(url_price)
        stores = [el.get_property('innerText')
                  for el in self.driver
                  .find_elements(by=By.CLASS_NAME, value='org-name')]
        prices = [el.get_property('innerText')
                    for el in self.driver.find_elements(by=By.CLASS_NAME,
                                                        value='org-price-c')]
        ids = [data['id'] for _ in range(len(stores))]
        names = [data['name'] for _ in range(len(stores))]
        return list(zip(ids, names, stores, prices))