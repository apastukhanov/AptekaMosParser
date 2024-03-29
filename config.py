from pathlib import Path

HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'JSESSIONID=9ff7c25d2b55503f4c2a2b3cf82a',
    'referer': 'https://aptekamos.ru/tovary',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
}

URL = "https://aptekamos.ru/tovary"

START_PAGE = 1
PAGES = 632

TITLE = 'AptekaMos Parser'
TAB_NAMES = ['Параметры отчета', 'Фильтры', 'Параметры загрузки']
DEFAULT_PATH = Path.home() / 'Downloads'
OPTIONS_STREAMS = [1, 3, 5, 7, 10, 15]
# OPTIONS_STREAMS = [1, 4, 8, 10, 14, 20]
OPTIONS_PROTOCOL = ['HTTP', 'HTTPS', 'SOCKS']

