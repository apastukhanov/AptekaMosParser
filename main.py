from presenter import Presenter
from view import MosAptekaGui

from model import Model

from aptekamos.parsers import BasicParser, MultiStreamsParser, WebBrowserParser
from sess import load_proxies, load_user_agents

def main():
    model = Model()
    view = MosAptekaGui()
    presenter = Presenter(model, view)
    presenter.run()
    # proxies = load_proxies()
    # proxies = None
    # ua = load_user_agents()
    # parser = BasicParser(streams_count=3, proxies=proxies, user_agents=ua)
    # parser = WebBrowserParser()
    # print(parser.collect_all_urls(4, model))
    # print(parser.collect_all_urls(3, model))
    # print(parser.collect_all_prices(model))


if __name__ == '__main__':
    main()