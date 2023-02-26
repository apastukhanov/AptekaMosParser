import tkinter as tk
from tkinter.filedialog import askdirectory
from typing import Callable
from functools import partial

from ttkwidgets.autocomplete import AutocompleteEntry

from db import fetchall

OFF_TEXT = "Speaker OFF"
ON_TEXT = "Speaker ON"
STATUS_UPDATE_TEXT = "Status Update"


db_resp = fetchall('urls', ['name', 'url'])
names = [x['name'] for x in db_resp]
urls = [x['url'] for x in db_resp]


class ParserGUIApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AptekaMos Parser")
        self.geometry("400x250+300+300")
        self.create_ui()
        self.speaker_on = True

    def create_ui(self) -> None:
        self.start_urLs_parse_button = tk.Button(
            self, text="Начать парсинг страниц", width=10, command=self.toggle
        )
        self.start_drugs_parse_button = tk.Button(
            self, text=OFF_TEXT, width=10, command=self.toggle
        )
        self.get_status_button = tk.Button(
            self, text=STATUS_UPDATE_TEXT, width=10, command=partial(self.display_status, text='Status is ok!')
        )
        self.select_folder_button = tk.Button(
            self, width=10, command=self.select_folder, text='Выбери папку для выгрузки файла')
        self.status_label = tk.Label(self, text="")
        self.entry = AutocompleteEntry(
            self,
            width=30,
            font=('Times', 18),
            completevalues=names)
        self.select_folder_button.pack()
        self.entry.pack()
        self.start_urLs_parse_button.pack()
        self.get_status_button.pack()
        self.status_label.pack()

    def toggle(self) -> None:
        self.start_urLs_parse_button.config(text=ON_TEXT if self.speaker_on else OFF_TEXT)
        self.speaker_on = not self.speaker_on
        indx = names.index(self.entry.get())
        msg = f'{urls[indx]}'
        self.display_status(text=msg)

    def select_folder(self) -> str:
        dir_path = askdirectory(
            parent=self,
            title="Browse File"
        )
        self.dir_path = dir_path
        print(dir_path)
        return dir_path

    def display_status(self, text: str) -> None:
        self.status_label.config(text=text)


if __name__ == '__main__':
    app = ParserGUIApp()
    app.mainloop()