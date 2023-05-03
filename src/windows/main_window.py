from tkinter import Tk, ttk, BOTH, END, LEFT, RIGHT, TOP, NS, Y, IntVar

import win32con
import win32gui

from src.functionality.windows_management import *


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Монитор окон")
        self.geometry("900x400")

        self.empty_filter = IntVar()

        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=True)

        self.windows_info_table = ttk.Treeview(self.container, show="headings", columns=("#1", "#2", "#3", "#4"))
        self.windows_info_table.grid(row=0, column=0, rowspan=12, columnspan=4, sticky="nsw")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        # self.windows_info_table.pack(fill=BOTH, expand=True)
        self.windows_info_table.heading("#1", text="HWND", command=lambda: self.sort(0, True, False))
        self.windows_info_table.heading("#2", text="Заголовок", command=lambda: self.sort(1, False, False))
        self.windows_info_table.heading("#3", text="Позиция", command=lambda: self.sort(2, False, False))
        self.windows_info_table.heading("#4", text="Размер", command=lambda: self.sort(3, False, False))

        def get_selected_hwnd():
            item_id = self.windows_info_table.focus()
            if item_id:
                item = self.windows_info_table.item(item_id)
                return item['values'][0]
            return -1

        def close_window():
            destroy_window(get_selected_hwnd())

            self.after(1000, self.update_table)

        def set_window_name():
            win32gui.SetWindowText(get_selected_hwnd(), self.window_name_entry.get())
            self.after(1000, self.update_table)

        def show_window():
            win32gui.ShowWindow(get_selected_hwnd(), win32con.SW_NORMAL)
            win32gui.SetForegroundWindow(get_selected_hwnd())

        def search_window():
            windows = get_windows()

            lines = []

            for window in enumerate(windows):
                line = (window[1][0], window[1][1],
                        (get_window_info(window[1][0])["x"], get_window_info(window[1][0])["y"]),
                        (get_window_info(window[1][0])["width"], get_window_info(window[1][0])["height"]))

                if self.search_window_entry.get() in window[1][1]:
                    lines.append(line)

            for row in self.windows_info_table.get_children():
                self.windows_info_table.delete(row)

            for line in lines:
                self.windows_info_table.insert("", END, values=line)

        def empty_filter_state():
            self.after(1000, self.update_table)

        self.destroy_button = ttk.Button(self.container, text="Destroy Window", command=close_window)
        self.destroy_button.grid(row=0, column=5, ipady=5, ipadx=5)

        self.show_window_button = ttk.Button(self.container, text="Show Window", command=show_window)
        self.show_window_button.grid(row=1, column=5, ipady=5, ipadx=5, pady=10)

        # self.destroy_button.pack(side=LEFT, fill=BOTH)
        self.window_name_entry = ttk.Entry(self.container)
        self.window_name_entry.grid(row=3, column=5, ipady=5, ipadx=5)

        # self.window_name_entry.pack(side=TOP, fill=BOTH)
        self.set_window_name_button = ttk.Button(self.container, text="Set Window Name", command=set_window_name)
        self.set_window_name_button.grid(row=4, column=5, ipady=5, ipadx=5)

        # self.set_window_name_button.pack(side=RIGHT, fill=BOTH)
        self.search_window_entry = ttk.Entry(self.container)
        self.search_window_entry.grid(row=6, column=5, ipady=5, ipadx=5)

        self.search_window_btn = ttk.Button(self.container, text="Search Window", command=search_window)
        self.search_window_btn.grid(row=7, column=5, ipady=5, ipadx=5)

        self.empty_filter_checkbutton = ttk.Checkbutton(self.container, text="Not empty", variable=self.empty_filter, command=empty_filter_state)
        self.empty_filter_checkbutton.grid(row=9, column=5, ipadx=5, ipady=5)

    def update_table(self):
        windows = get_windows()

        lines = []

        for window in enumerate(windows):
            line = (window[1][0], window[1][1],
                    (get_window_info(window[1][0])["x"], get_window_info(window[1][0])["y"]),
                    (get_window_info(window[1][0])["width"], get_window_info(window[1][0])["height"]))
            if self.empty_filter.get() == 1:
                if window[1][1] != '':
                    lines.append(line)

            elif self.empty_filter.get() == 0:
                lines.append(line)

        for row in self.windows_info_table.get_children():
            self.windows_info_table.delete(row)

        for line in lines:
            print(line)
            self.windows_info_table.insert("", END, values=line)

    def sort(self, col, is_num, reverse):
        l = []
        if is_num:
            l = [(int(self.windows_info_table.set(k, col)), k) for k in self.windows_info_table.get_children("")]
        else:
            l = [(self.windows_info_table.set(k, col), k) for k in self.windows_info_table.get_children("")]
        # сортируем список
        l.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index, (_, k) in enumerate(l):
            self.windows_info_table.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        self.windows_info_table.heading(col, command=lambda: self.sort(col, is_num, not reverse))
