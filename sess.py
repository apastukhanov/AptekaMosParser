from functools import partial

from random import choice

import requests
from typing import Dict

from config import HEADERS, URL


sess = requests.Session()
sess.headers.update(HEADERS)


def get_session() -> requests.Session:
    return sess


def get_page_source(url: str,
                    params: Dict = None,
                    is_proxy: bool = False):
    if is_proxy:
        ua = choice(load_user_agents())
        proxy = choice(load_proxies())
        return _get_page_html(url, params, user_agent=ua, proxy=proxy)
    return _get_page_html(url, params)


def _get_page_html(url: str,
                    params: Dict = None,
                    user_agent: str = None,
                    proxy: str = None) -> str:
    if user_agent:
        sess.headers['user-agent'] = user_agent
    req_fn = sess.get
    if params:
        req_fn = partial(sess.get, params=params)
    if proxy:
        req_fn = partial(req_fn, proxies={'https': 'https://' + proxy})
    html = req_fn(url).text
    save_html(html)
    return html


def save_html(html: str):
    with open('response.html', 'w') as f:
        f.write(html)


def load_user_agents():
    with open('user_agents.txt', 'r') as f:
        ua = f.read()
    return ua.split('\n')


def load_proxies():
    with open('proxies.txt', 'r') as f:
        proxies = f.read()
    return proxies.split('\n')


def main():
    print(load_user_agents())
    print(load_proxies())


# main()