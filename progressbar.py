from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo


class ProgressBar(tk.Tk):
    def __init__(self, total: int, name: str):
        super().__init__()
        self.total = total
        self.name = name
        self.geometry('300x120+500+400')
        self.title('Progress')
        self.resizable(height=False, width=False)
        self.style = ttk.Style(self)
        self.style.theme_use('classic')
        self._create_ui()

    def _create_ui(self):
        self.value_var = tk.IntVar(value=0)
        self.pb = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            length=286,
            variable=self.value_var
        )
        self.pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        self.pb['maximum'] = self.total
        self.value_label = ttk.Label(self, text=self.update_progress_label())
        self.value_label.grid(column=0, row=1, columnspan=2)

    def update(self):
        self.value_var.set(self.value_var.get() + 1)
        self.pb['value'] = self.value_var.get()
        self.value_label['text'] = self.update_progress_label()
        self.pb.update()

    def close(self):
        self.pb.stop()
        self.value_label['text'] = self.update_progress_label()
        # showinfo('dfsg', 'sdfg')
        self.destroy()

    def update_progress_label(self):
        return f"Загрузка {self.name}: {self.value_var.get() / self.total * 100: .2f}%"