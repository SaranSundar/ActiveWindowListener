import os
import time

import win32api
import win32con
import win32gui
import win32ui

from apis.input_methods.mouse_and_keyboard_listener import parse_window_name_from_task_manager, \
    parse_window_name_from_details
from apis.monitoring_details.active_window_details import get_active_window, get_open_windows_in_task_manager


def log_window_details():
    start_time = time.time()
    current_active_window_details = get_active_window()
    end_time = time.time()
    print("Active window is")
    current_active_window_name = parse_window_name_from_details(current_active_window_details)
    if current_active_window_name == "" or len(current_active_window_name) <= 2:
        current_active_window_name = current_active_window_details
    print(current_active_window_name)
    print("--- %s seconds for getting active window ---" % (end_time - start_time))
    start_time = time.time()
    open_windows = get_open_windows_in_task_manager()
    if len(open_windows) >= 2:
        open_windows = open_windows[2:]
    for i in range(len(open_windows)):
        open_windows[i] = parse_window_name_from_task_manager(open_windows[i])
    end_time = time.time()
    print("Open windows is")
    print(open_windows)
    print("--- %s seconds for getting windows in task manager ---" % (end_time - start_time))
    print("")
    print("")
    print("")


def save_icon(icon_path, save_path):
    if icon_path == "Error: No path found":
        return

    icon_path = icon_path.replace("\\", "/")
    try:
        iconX = win32api.GetSystemMetrics(win32con.SM_CXICON)
        iconY = win32api.GetSystemMetrics(win32con.SM_CXICON)

        large, small = win32gui.ExtractIconEx(icon_path, 0)
        win32gui.DestroyIcon(small[0])

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, iconX, iconX)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        from PIL import Image
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmpstr, 'raw', 'BGRA', 0, 1
        )
        img.save(save_path)
    except Exception as e:
        print("Error:")
        print(e)


def find_all_icons():  # Create a function for later.
    for name in os.listdir("C://Program Files//7-Zip"):
        if name.lower().endswith('.exe'):
            print(name)
            save_icon("C://Program Files//7-Zip//" + name, name)


if __name__ == '__main__':
    while True:
        log_window_details()
        time.sleep(0.5)
