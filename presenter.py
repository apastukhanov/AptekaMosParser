from __future__ import annotations
from typing import Protocol


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

    def click_get_prices(self):
        pass

    def click_add_filter(self):
        pass

    def click_clear_filters(self):
        pass

    def click_add_filters_from_file(self):
        pass

    def click_add_proxy(self):
        pass

    def click_clear_proxies(self):
        pass

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
        self._on_open()
        # self.update_task_list()
        self.view.mainloop()