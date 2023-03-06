import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog

from ttkwidgets.autocomplete import AutocompleteEntry

from typing import Protocol

from config import (
    TITLE,
    TAB_NAMES,
    DEFAULT_PATH,
    OPTIONS_STREAMS,
    OPTIONS_PROTOCOL
)


class Presenter(Protocol):
    def click_get_prices(self):
        ...

    def click_add_filter(self):
        ...

    def click_clear_filters(self):
        ...

    def click_add_filters_from_file(self):
        ...

    def click_add_proxy(self):
        ...

    def click_clear_proxies(self):
        ...

    def print_menu_box_value(self) -> None:
        """print(self.is_url_parsed.get())"""
        ...


class MosAptekaGui(tk.Tk):
    """GUI для настройки парсера сайта https://aptekamos.ru/"""
    def __init__(self) -> None:
        super().__init__()
        self.title(TITLE)
        self.geometry("570x480+400+300")
        self.resizable(height=False, width=False)
        self.style = ttk.Style(self)
        self.style.theme_use('classic')
        self.style.configure('Test.TLabel', background='white')

    def init_ui(self, presenter: Presenter) -> None:
        tab_control = ttk.Notebook(self)
        tab1, tab2, tab3 = tk.Frame(tab_control), \
            tk.Frame(tab_control), tk.Frame(tab_control)
        for i, tab in enumerate([tab1, tab2, tab3]):
            tab.grid()
            tab_control.add(tab, text=TAB_NAMES[i])
        r_info = self._create_main_menu(tab1, presenter)
        status_info = self._create_status_bar(tab1, presenter)
        fltr_info = self._create_filter_tab(tab2, presenter)
        engine_info = self._create_parse_settings_tab(tab3)
        proxies_info = self._create_proxies_list_box(tab3, presenter)
        for i in range(3):
            r_info.columnconfigure(i, weight=1)
            status_info.columnconfigure(i, weight=1)
            fltr_info.columnconfigure(i, weight=1)
        for el in [r_info, fltr_info, status_info, engine_info,
                   proxies_info, tab_control]:
            el.pack(fill='both')

    @property
    def bg(self) -> str:
        return self.style.lookup('TFrame', 'background')

    def _create_main_menu(self, tab: ttk.Notebook, presenter: Presenter):
        r_info = ttk.LabelFrame(tab, text='\nГлавное меню программы\n')
        ttk.Label(r_info, text='Путь сохранения Excel:').grid(row=0, column=0)
        self.main_menu_path_label = tk.Label(r_info, text=DEFAULT_PATH, anchor=tk.W,
                                             width=30, background='white')
        self.main_menu_path_label.grid(row=0, column=1)
        ttk.Button(r_info, text='Изменить', command=self._click_change_excel_path)\
            .grid(row=0, column=2)
        ttk.Button(r_info, text='Скачать цены', command=presenter.click_get_prices)\
            .grid(row=1, column=0, columnspan=2, padx=20, sticky=tk.E+tk.W)
        self.is_url_parsed = tk.IntVar()
        self.main_menu_box = tk.Checkbutton(r_info, text='Обновить url',
                                            variable=self.is_url_parsed,
                                            onvalue=1,
                                            offvalue=0,
                                            command=presenter.print_menu_box_value,
                                            bg=self.bg)
        self.main_menu_box.grid(row=1, column=2, pady=20)
        return r_info

    def _create_status_bar(self, tab: ttk.Notebook, presenter: Presenter):
        r_info = ttk.LabelFrame(tab, text='\nЛоги\n')
        self.status_str = tk.StringVar()
        self.status_str = ""
        self.status_label = tk.Listbox(r_info, height=11,
                                       font=('Times New Roman', 17),
                                       background=self.bg,
                                       activestyle='none')
        self.status_label.grid(row=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S, padx=10, pady=5)
        return r_info

    def _create_filter_tab(self, tab: ttk.Notebook, presenter: Presenter):
        r_info = ttk.LabelFrame(tab, text='\nСписок исключений\n')
        names = presenter.model.fetchall('urls', ['name'])
        entries = [x['name'] for x in names] if names else []
        self.entry = AutocompleteEntry(r_info, width=30, completevalues=entries)
        self.entry.grid(row=0, column=0, sticky=tk.E+tk.W, columnspan=3, padx=10)
        self.entry.bind("<Return>", presenter.click_add_filter)
        scrollbar = tk.Scrollbar(r_info)
        scrollbar.grid(row=1, column=4, sticky=tk.N + tk.S, pady=5)
        ttk.Button(r_info, text='Добавить исключение',
                   command=presenter.click_add_filter)\
            .grid(row=0, column=3, sticky=tk.E+tk.W, padx=10)
        self.flts_list = tk.Listbox(r_info, height=15,
                                    font=('Times New Roman', 17),
                                    activestyle='none')
        self.flts_list.grid(row=1, column=0,
                            columnspan=4,
                            sticky=tk.E+tk.W+tk.N+tk.S, padx=10)
        self.flts_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.flts_list.yview)
        ttk.Button(r_info, text='Очистить исключения', command=presenter.click_clear_filters)\
            .grid(row=2, column=0, padx=10, sticky=tk.W)
        ttk.Button(r_info, text='Загрузить исключения из файла',
                   command=presenter.click_add_filters_from_file)\
            .grid(row=2, column=1, columnspan=3, sticky=tk.E+tk.W, padx=10)
        return r_info

    def _create_parse_settings_tab(self, tab: ttk.Notebook):
        r_info = ttk.LabelFrame(tab, text='\nВыбор Парсера\n')
        self.parser_type = tk.IntVar()
        self.parser_type.set(1)
        tk.Radiobutton(r_info,
                       text='Безопасная загрузка', anchor=tk.W, variable=self.parser_type,
                       value=0, bg=self.bg, command=self.selected_safe_parsing)\
            .grid(row=0, column=0, sticky=tk.W+tk.E, pady=10)
        tk.Radiobutton(r_info,
                       text='Быстрая загрузка', anchor=tk.W, variable=self.parser_type,
                       value=1, bg=self.bg, command=self.selected_fast_parsing)\
            .grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)

        tk.Label(r_info, text='Количество потоков', bg=self.bg)\
            .grid(row=2, column=0, pady=10, padx=5)
        self.streams_count = tk.IntVar(r_info)
        self.streams_count.set(OPTIONS_STREAMS[0])
        self.stream_option_menu = \
            tk.OptionMenu(r_info, self.streams_count, *OPTIONS_STREAMS)
        self.stream_option_menu.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.is_proxy = tk.IntVar(r_info)
        self.is_proxy.set(0)
        self.proxy_checkbtn = tk.Checkbutton(r_info, text='Использовать прокси',
                                             variable=self.is_proxy,
                                             onvalue=1,
                                             offvalue=0, bg=self.bg)
        self.proxy_checkbtn.grid(row=3, column=0, sticky=tk.W + tk.E)

        return r_info

    def _create_proxies_list_box(self, tab: ttk.Notebook, presenter: Presenter):
        r_info = ttk.LabelFrame(tab, text='\nНастройка прокси\n')
        proxy = tk.StringVar()
        self.proxy_entry = ttk.Entry(r_info, width=30, textvariable=proxy)
        self.proxy_entry.grid(row=0, column=0, sticky=tk.E + tk.W, padx=10)
        var1 = tk.StringVar(r_info)
        var1.set(OPTIONS_PROTOCOL[0])
        tk.OptionMenu(r_info, var1, *OPTIONS_PROTOCOL).grid(row=0, column=1)
        ttk.Button(r_info, text='Добавить прокси', command=presenter.click_add_proxy) \
            .grid(row=0, column=2, sticky=tk.E + tk.W, padx=10)
        scrollbar = tk.Scrollbar(r_info)
        scrollbar.grid(row=1, column=4, sticky=tk.N + tk.S + tk.E, pady=5, padx=5)
        self.proxies_list = tk.Listbox(r_info, height=5,
                                       font=('Times New Roman', 17))
        self.proxies_list.grid(row=1, column=0,
                               columnspan=4,
                               sticky=tk.E + tk.W + tk.N + tk.S, padx=5)
        self.proxies_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.proxies_list.yview)
        ttk.Button(r_info, text='Очистить прокси',
                   command=presenter.click_clear_proxies)\
            .grid(row=2, column=0, padx=10, sticky=tk.W)
        return r_info

    def selected_safe_parsing(self):
        self.proxy_checkbtn.config(state='disabled')
        self.stream_option_menu.config(state='disabled')

    def selected_fast_parsing(self):
        self.proxy_checkbtn.config(state='active')
        self.stream_option_menu.config(state='active')

    def _click_change_excel_path(self):
        file_path = filedialog.askdirectory(initialdir=str(DEFAULT_PATH))
        if file_path:
            self.main_menu_path_label.config(text=file_path)

    def get_entry_text(self) -> str:
        pass

    def clear_entry(self) -> None:
        pass

    def update_proxies_list(self, proxies: list[str]) -> None:
        for proxy in proxies:
            self.proxies_list.insert(tk.END, proxy)

    def delete_filters_list(self):
        self.flts_list.delete(0, tk.END)

    def update_status(self, status_text):
        self.status_label.insert(tk.END, status_text)

    def update_filters_list(self, filters: list[str]) -> None:
        self.delete_filters_list()
        for fltr in filters:
            self.flts_list.insert(tk.END, fltr)