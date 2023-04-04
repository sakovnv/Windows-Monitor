from tkinter import Tk, ttk, BOTH, END


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Монитор окон")
        self.geometry("800x600")

        self.windows_info_table = ttk.Treeview(columns=("HWND", "Title", "Size", "Position"))
        self.windows_info_table.pack(fill=BOTH, expand=True)

        self.windows_info_table.heading("HWND", text="HWND")
        self.windows_info_table.heading("Title", text="Заголовок")
        self.windows_info_table.heading("Size", text="Размер")
        self.windows_info_table.heading("Position", text="Позиция")

    def update_table(self, lines: list):
        for line in lines:
            self.windows_info_table.insert("", END, values=line)
