import os
import time
from threading import Thread

import win32api
import win32con
import win32gui
import win32ui
import glob


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
            encoded_file_path = filename.replace("\\", "-'backslash'-")
            # "Encodes" the file_path so that it can be saved and decoded later
            encoded_file_path = encoded_file_path.replace(":", "-'colon'-")
            result = save_icon(filename, "./icons/" + encoded_file_path + ".png")
            if result:
                print("Saved " + name, " path: " + filename)
            else:
                print("Error on " + name, " path: " + filename)
            print(filename)
        print("********************")
        print("")

    search_path("C:\\Program Files\\")
    search_path("C:\\Program Files (x86)\\")
    end_time = time.time()
    print("--- %s seconds for finding and saving all icons ---" % (end_time - start_time))


def find_icon_from_path(path):
    path = path[:-3]
    path = path.replace("\\", "-'backslash'-")
    path = path.replace(":", "-'colon'-")
    for file in os.listdir("./icons"):
        if file.startswith(path):
            print(file)
            return file  # Returns png filename
    print("EXE icon not found")


def parse_exe_name(exe_name):
    exe_split = exe_name.split("\\")
    return exe_split[2] + " " + exe_split[-1].split(".exe")[0]


find__and_save_all_icons()
