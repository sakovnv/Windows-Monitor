from src.functionality.windows_management import *
from src.windows.main_window import MainWindow


def main():
    windows = get_windows()

    lines = []

    for window in enumerate(windows):
        line = (window[1][0], window[1][1],
                (get_window_info(window[1][0])["x"], get_window_info(window[1][0])["y"]),
                (get_window_info(window[1][0])["width"], get_window_info(window[1][0])["height"]))
        lines.append(line)

    main_window = MainWindow()
    main_window.update_table(lines)
    main_window.mainloop()

    hwnd = select_window(windows, 1)

    window_info = get_window_info(hwnd)

    print(
        f"Окно '{window_info['title']}' имеет размер {window_info['width']}x{window_info['height']} и находится на позиции ({window_info['x']}, {window_info['y']})")


if __name__ == '__main__':
    main()
