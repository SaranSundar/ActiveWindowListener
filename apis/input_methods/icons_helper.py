import glob
import os
import pathlib
import time

import win32api
import win32con
import win32gui
import win32ui
# pip install Pillow did not work well with pyinstaller since the name was PIL for the from, so I just copied the site package folder into here
from apis.input_methods.PIL import Image


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
        print("Error:")
        print(e)
        return False


def find__and_save_all_icons(file_path="icons"):
    start_time = time.time()
    os.makedirs(file_path)

    def search_path(pathname):
        for filename in glob.iglob(pathname + '**/*.exe', recursive=True):
            name = parse_exe_name(filename)
            encoded_file_path = filename.replace("\\", "-'backslash'-")
            # "Encodes" the file_path so that it can be saved and decoded later
            encoded_file_path = encoded_file_path.replace(":", "-'colon'-")
            result = save_icon(filename, file_path + "/" + encoded_file_path + ".png")
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
    icons_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), 'icons')
    for file in os.listdir(icons_folder):
        if file.startswith(path):
            return file
    print("EXE icon not found")
    return ""


def parse_exe_name(exe_name):
    exe_split = exe_name.split("\\")
    return exe_split[2] + " " + exe_split[-1].split(".exe")[0]

# find__and_save_all_icons()
# print(find_icon_from_path("C:\\Program Files\\JetBrains\\PyCharm Community Edition 2019.2.3\\bin\\pycharm64.exe"))
