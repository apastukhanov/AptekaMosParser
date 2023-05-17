import logging

from model import Model

from aptekamos.parsers import (
    BasicParser,
    MultiStreamsParser,
    WebBrowserParser,
    download_drugs_info
)

from excel_processor import (
    create_output_excel,
    save_excel
)


logging.basicConfig(level=logging.INFO)


PARSERS = {
    'safe': WebBrowserParser,
    'basic': BasicParser,
    'multi': MultiStreamsParser
}


def read_settings(model):
    settings = model.fetchall('gui_settings',
                                    ['excel_path', 'is_url_parsed',
                                    'parser_type', 'streams_count',
                                    'is_proxy'])
    return settings[0]


def get_parser(settings):
    if settings['parser_type'] == 0:
        parser = PARSERS['safe']()
    else:
        if settings['streams_count'] > 1:
            parser = PARSERS['multi'](settings['streams_count'])
        else:
            parser = PARSERS['basic']()
    return parser


def get_prices():
    model = Model()
    settings = read_settings(model)
    logging.info(settings)
    parser = get_parser(settings)
    logging.info('Скачивание urls...')
    page_count = download_drugs_info(model)
    page_count = 5
    parser.collect_all_urls(page_count, model)
    logging.info('Скачивание url завершено!')
    logging.info('Скачивание цен началось...')
    parser.collect_all_prices(model)
    logging.info('Скачивание цен завершено!')
    df = create_output_excel(model)
    dir_path = settings['excel_path']
    logging.info(f'Записать данных в Excel файл начата...')
    save_excel(df=df, dir_path=dir_path)
    logging.info(f'Excel c ценами сохранен '
                 f'в папку: {dir_path}')



if __name__ == '__main__':
    get_prices()