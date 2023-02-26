from presenter import Presenter
from view import MosAptekaGui

from model import Model


def main():
    model = Model()
    view = MosAptekaGui()
    presenter = Presenter(model, view)
    presenter.run()


if __name__ == '__main__':
    main()