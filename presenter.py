from __future__ import annotations

import re
from typing import Protocol

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


PARSERS = {
    'safe': WebBrowserParser,
    'basic': BasicParser,
    'multi': MultiStreamsParser
}


class Model(Protocol):
    def _init_db(self):
        ...


class View(Protocol):
    def init_ui(self, presenter: Presenter) -> None:
        ...

    def get_entry_text(self) -> str:
        ...

    def clear_entry(self) -> None:
        ...

    def update_task_list(self, tasks: list[str]) -> None:
        ...

    @property
    def bg(self) -> str:
        ...

    def mainloop(self) -> None:
        ...


class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.view.protocol('WM_DELETE_WINDOW', self._on_close)

    def handle_add_task(self, event=None) -> None:
        task = self.view.get_entry_text()
        self.view.clear_entry()
        self.model.add_task(task)
        self.update_task_list()

    def handle_delete_task(self, event=None) -> None:
        self.model.delete_task(self.view.selected_task)
        self.update_task_list()

    def update_task_list(self) -> None:
        tasks = self.model.get_tasks()
        self.view.update_task_list(tasks)

    def get_parser(self):
        if self.view.parser_type.get() == 0:
            parser = PARSERS['safe']()
        else:
            if self.view.streams_count.get() > 1:
                parser = PARSERS['multi'](self.view.streams_count.get())
            else:
                parser = PARSERS['basic']()
        return parser

    def click_get_prices(self):
        parser = self.get_parser()
        ua = [d['user_agent'] for d in 
              self.model.fetchall('user_agents', ['user_agent'])]
        parser.set_user_agents(ua)
        if self.view.is_url_parsed.get():
            self.view.update_status('Скачивание urls...')
            page_count = download_drugs_info(self.model)
            page_count = 3
            parser.collect_all_urls(page_count, self.model)
            self.view.update_status('Скачивание urls завершено!')
        self.view.update_status('Скачивание цен началось...')
        parser.collect_all_prices(self.model)
        self.view.update_status('Скачивание цен завершено!')
        df = create_output_excel(self.model)
        dir_path = self.view.main_menu_path_label.cget('text')
        self.view.update_status(f'Записать данных в Excel файл начата...')
        save_excel(df=df, dir_path=dir_path)
        self.view.update_status(f'Excel c ценами сохранен '
                                f'в папку: {dir_path}')

    def click_add_filter(self, event=None):
        name = self.view.entry.get()
        if name == '':
            return
        cols = ['url', 'name']
        urls = self.model.fetchall('urls', cols)
        filters = self.model.fetchall('filters', cols)
        urls_search = list(filter(lambda x: x['name'] == name, urls))
        filters_search = list(filter(lambda x: x['name'] == name, filters))
        if not filters_search:
            self.model.insert('filters', cols, [(urls_search[0]['url'],
                                                 urls_search[0]['name'])])
        self.view.entry.delete(0, len(name))
        self.update_filters()

    def update_filters(self):
        cols = ['url', 'name']
        filters = [f"{i+1}) {x['name']}" for i, x in
                   enumerate(self.model.fetchall('filters', cols))]
        if filters:
            self.view.update_filters_list(filters)

    def update_proxies(self):
        cols = ['ip', 'port', 'proxy_type']
        proxies = [f"{i+1}) {x['ip']} {x['port']} {x['proxy_type']}" for i, x in
                   enumerate(self.model.fetchall('proxies', cols))]
        if proxies:
            self.view.update_proxies_list(proxies)

    def click_clear_filters(self):
        self.model.clear_table('filters')
        self.view.delete_filters_list()

    def click_add_filters_from_file(self):
        pass

    def click_add_proxy(self):
        pattern = re.compile('\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}:\d{2,8}')
        user_input = self.view.proxy_entry.get()
        search = pattern.findall(user_input)
        if search:
            ip, port = search[0].split(':')
            proxy_type = self.view.proxy_type.get()
            ips = self.model.fetchall('proxies', ['ip'])
            if not list(filter(lambda x: x['ip'] == ip, ips)):
                cols = ['ip', 'port', 'proxy_type']
                self.model.insert('proxies', cols, [(ip, port, proxy_type)])
                self.update_proxies()
                self.view.proxy_entry.delete(0, len(user_input))

    def click_clear_proxies(self):
        self.model.clear_table('proxies')
        self.view.delete_proxies_list()

    def print_menu_box_value(self) -> None:
        """print(self.is_url_parsed.get())"""
        pass

    def _on_close(self):
        self._save_view_settings()
        self.view.destroy()

    def _on_open(self):
        settings = self.model.fetchall('gui_settings',
                                       ['excel_path', 'is_url_parsed',
                                        'parser_type', 'streams_count',
                                        'is_proxy'])
        if settings:
            self.view.main_menu_path_label.config(text=settings[0]['excel_path'])
            self.view.is_url_parsed.set(settings[0]['is_url_parsed'])
            self.view.parser_type.set(settings[0]['parser_type'])
            self.view.streams_count.set(settings[0]['streams_count'])
            self.view.is_proxy.set(settings[0]['is_proxy'])
            if not settings[0]['parser_type']:
                self.view.selected_safe_parsing()

    def _save_view_settings(self):
        settings = {'excel_path': self.view.main_menu_path_label.cget('text'),
                    'is_url_parsed': self.view.is_url_parsed.get(),
                    'parser_type': self.view.parser_type.get(),
                    'streams_count': self.view.streams_count.get(),
                    'is_proxy': self.view.is_proxy.get()}
        self.model.clear_table('gui_settings')
        self.model.insert('gui_settings', list(settings.keys()), [tuple(settings.values())])

    def run(self) -> None:
        self.view.init_ui(self)
        self.update_filters()
        self.update_proxies()
        self._on_open()
        # self.update_task_list()
        self.view.mainloop()