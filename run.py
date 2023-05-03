from src.functionality.windows_management import *
from src.windows.main_window import MainWindow


def main():

    main_window = MainWindow()
    main_window.after(1000, main_window.update_table)
    main_window.mainloop()


if __name__ == '__main__':
    main()
