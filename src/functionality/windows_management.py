import win32con
import win32gui


def get_windows():
    all_windows = []

    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        return True
    win32gui.EnumWindows(callback, all_windows)
    return all_windows


def select_window(windows, item):

    return windows[item][0]


def get_window_info(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    title = win32gui.GetWindowText(hwnd)
    return {"hwnd": hwnd, "title": title, "x": rect[0], "y": rect[1], "width": rect[2] - rect[0],
            "height": rect[3] - rect[1]}


def destroy_window(hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
