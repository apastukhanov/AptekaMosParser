from time import sleep
from multiprocessing import Pool

from aptekamos.parsers import download_drugs_info
from model import Model


def save_html(html: str):
    with open('output/response.html', 'w') as f:
        f.write(html)


def load_user_agents():
    with open('user_agents.txt', 'r') as f:
        ua = f.read()
    return ua.split('\n')


def load_proxies():
    with open('proxies.txt', 'r') as f:
        proxies = f.read()
    return proxies.split('\n')


def long_func(i: int):
    sleep(1)
    if i == 7:
        raise NameError
    return i


def main():
    model = Model()
    download_drugs_info(model)
    # with Pool(3) as p:
    #     output = []
    #     try:
    #         for res in p.imap(long_func, range(100)):
    #             print(res)
    #             output.append(res)
    #     except:
    #         print(output)




if __name__=='__main__':
    main()