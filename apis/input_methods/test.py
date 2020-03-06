import os
import time

import win32api
import win32con
import win32gui
import win32ui
import glob

from apis.monitoring_details.active_window_details import get_active_window, get_open_windows_in_task_manager


def parse_window_name_from_details(window_string):
    split_window_name = window_string.split(' - ')
    split_window_name = split_window_name[len(split_window_name) - 1]
    return split_window_name


def parse_window_name_from_task_manager(window_string):
    # print("WINDOW STRING IS")
    # print(window_string)
    split_window_name = window_string.split(' ')
    split_window_name = " ".join(split_window_name[0:10]).strip()
    if len(split_window_name) > len("Microsoft Edge Content Process"):
        new_name = split_window_name.split(" ")
        split_window_name = ""
        for word in new_name:
            if len(split_window_name) + len(word) <= len("Microsoft Edge Content Process"):
                split_window_name += " " + word
                split_window_name = split_window_name.strip()
            else:
                break
        if split_window_name == "":
            if len(window_string) >= len("Microsoft Edge Content Process"):
                split_window_name = window_string[0:len("Microsoft Edge Content Process")] + "..."
            else:
                split_window_name = window_string
            # ignore above
            split_window_name = None
    # print("PARSED STRING IS")
    # print(split_window_name)
    return split_window_name


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
        return False

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
        extrema = img.convert("L").getextrema()
        if "Chrome" in icon_path:
            print("TEST")
        if extrema[1] < 250:
            img.save(save_path)
        return True
    except Exception as e:
        return False
        # print("Error:")
        # print(e)


def find__and_save_all_icons():
    start_time = time.time()

    def search_path(pathname):
        for filename in glob.iglob(pathname + '**/*.exe', recursive=True):
            name = parse_exe_name(filename)
            result = save_icon(filename, "./icons/" + name + ".png")
            if result:
                print("Saved " + name, " path: " + filename)
                print("")
            else:
                print("Error on " + name, " path: " + filename)
        print("********************")
    search_path("C:\\Program Files\\")
    search_path("C:\\Program Files (x86)\\")
    end_time = time.time()
    print("--- %s seconds for finding and saving all icons ---" % (end_time - start_time))


def parse_exe_name(exe_name):
    exe_split = exe_name.split("\\")
    return exe_split[2] + " " + exe_split[-1].split(".exe")[0]


def test_windows():
    while True:
        log_window_details()
        time.sleep(0.5)


if __name__ == '__main__':
    find__and_save_all_icons()
