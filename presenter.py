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

    def run(self) -> None:
        self.view.init_ui(self)
        # self.update_task_list()
        self.view.mainloop()