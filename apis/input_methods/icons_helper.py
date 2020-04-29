import glob
import os
import pathlib
import platform
import sys
import time

import win32api
import win32con
import win32gui
import win32ui


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
        from PIL import Image
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmpstr, 'raw', 'BGRA', 0, 1
        )
        extrema = img.convert("L").getextrema()
        if "Chrome" in icon_path:
            pass
            #print("TEST")
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
<<<<<<< HEAD
            encoded_file_path = filename
            encoded_file_path = filename.replace("\\", "-{]{-")
            # "Encodes" the file_path so that it can be saved and decoded later
            encoded_file_path = encoded_file_path.replace(":", "-(})")
=======
            encoded_file_path = filename.replace("\\", "@##")
            # "Encodes" the file_path so that it can be saved and decoded later
            encoded_file_path = encoded_file_path.replace(":", "@;;")
>>>>>>> a911750a6b50ba9d4754f293ff4361db1804f012
            result = save_icon(filename, file_path + "/" + encoded_file_path + ".png")
            if result:
                print("Saved " + name, " path: " + file_path + "/" + encoded_file_path)
            else:
                print("Error on " + name, " path: " + file_path + "/" + encoded_file_path)
            print(filename)
        #print("********************")
        #print("")

    search_path("C:\\Program Files\\")
    search_path("C:\\Program Files (x86)\\")
    end_time = time.time()
    print("--- %s seconds for finding and saving all icons ---" % (end_time - start_time))


def find_icon_from_path(path):
    path = path[:-3]
<<<<<<< HEAD
    path = path.replace("\\", "-{]{-")
    path = path.replace(":", "-(})")
    operating_system = str(platform.system()).lower()
    icon_folder = None
    if getattr(sys, 'frozen', False):
        if "window" in operating_system:
            static_folder = os.path.join(sys._MEIPASS, 'static', 'icons')
            icons_folder = static_folder
    else:
        icons_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), 'icons')
=======
    path = path.replace("\\", "@##")
    path = path.replace(":", "@;;")
    icons_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), 'icons')
>>>>>>> a911750a6b50ba9d4754f293ff4361db1804f012
    for file in os.listdir(icons_folder):
        if file.startswith(path):
            return file
    #print("EXE icon not found")
    return ""


def parse_exe_name(exe_name):
    exe_split = exe_name.split("\\")
    return exe_split[2] + " " + exe_split[-1].split(".exe")[0]


if __name__ == '__main__':
    find__and_save_all_icons()

# find__and_save_all_icons()
# print(find_icon_from_path("C:\\Program Files\\JetBrains\\PyCharm Community Edition 2019.2.3\\bin\\pycharm64.exe"))
