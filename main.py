from presenter import Presenter
from view import MosAptekaGui

from model import Model

from aptekamos.parsers import BasicParser, MultiStreamsParser

def main():
    model = Model()
    # view = MosAptekaGui()
    # presenter = Presenter(model, view)
    # presenter.run()
    parser = MultiStreamsParser(3)
    print(parser.collect_all_prices(model))

if __name__ == '__main__':
    main()