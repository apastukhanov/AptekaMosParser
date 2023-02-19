import requests

from config import HEADERS


sess = requests.Session()
sess.headers.update(HEADERS)


def get_session() -> requests.Session:
    return sess