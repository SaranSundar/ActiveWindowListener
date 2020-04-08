import logging
import sys
import time
from datetime import datetime, timedelta

from apis.monitoring_details.win32_window_details import active_window_process, all_open_windows

if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32api
    import win32con
    import win32gui
    import win32ui
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

from apis.mongo.mongo_client import log_event, log_processes
from apis.monitoring_details.active_window_details import \
    get_active_window, get_open_windows_in_task_manager, get_path_from_pid

logging.basicConfig(filename="../window_log.txt", level=logging.DEBUG, format='%(message)s')

MOUSE_MOVE = "MOUSE_MOVE"
MOUSE_CLICK = "MOUSE_CLICK"
MOUSE_SCROLL = "MOUSE_SCROLL"
KEYBOARD_RELEASE = "KEYBOARD_RELEASE"
KEYBOARD_PRESS = "KEYBOARD_PRESS"

event_types = {
    KEYBOARD_PRESS: 0,
    KEYBOARD_RELEASE: 1,
    MOUSE_MOVE: 2,
    MOUSE_CLICK: 3,
    MOUSE_SCROLL: 4,
}

current_event_type = None
prev_event_type = None
active_window_details = None
active_windows = []
last_time = datetime.utcnow()


def log_window_details():
    global active_window_details
    global active_windows  # type: list
    global prev_event_type
    time.sleep(0.0001)

    # Updates closed and opened windows
    current_active_window_details = get_active_window()
    current_active_window_name = None
    if current_active_window_details is not None:
        # This is for checking diff in applications but not events
        if current_active_window_details != active_window_details:
            start_time = time.time()
            open_windows = []
            # On windows we want to use window name from task manager, but on mac we only have current window name
            if sys.platform in ['Windows', 'win32', 'cygwin']:
                open_windows = get_open_windows_in_task_manager()
                if len(open_windows) > 2:
                    open_windows = open_windows[2:]
            else:
                # On windows current_details is a lot more in depth, on mac its just the app name
                open_windows.append(current_active_window_details)
            end_time = time.time()
            print("--- %s seconds for getting open windows ---" % (end_time - start_time))
            # Logs all windows that have been closed
            print("OPEN WINDOWS IS")
            print(open_windows)
            for i in range(len(active_windows) - 1, -1, -1):
                found_window = False
                for ow in open_windows:
                    if active_windows[i] in ow:
                        found_window = True
                        break
                if found_window is False:
                    print(active_windows[i] + " is no longer open")
                    logging.info(active_windows[i] + " is no longer open")
                    del active_windows[i]
            start_time = time.time()
            # Adds any new windows to the list
            for w in range(len(open_windows)):
                process_id = get_PID(open_windows[w])  # Gets PID from task manager
                windows_path = get_path_from_pid(process_id)  # Gets exe path of window
                get_image_from_path(windows_path, process_id)  # Gets image from exe path
                open_windows[w] = parse_window_name_from_task_manager(open_windows[w])
                if open_windows[w] is None:
                    continue
                found_window = False
                for aw in active_windows:
                    if open_windows[w] in aw:
                        found_window = True
                        break
                if found_window is False:
                    # print(window + " is now added to the list of open windows")
                    print(open_windows[w] + " is now added to the list of open windows")
                    active_windows.append(open_windows[w])
                    logging.info(open_windows[w] + " is now added to the list of open windows")
            print("ACTIVE WINDOWS IS")
            print(active_windows)
            end_time = time.time()
            print("--- %s seconds for getting active windows ---" % (end_time - start_time))

        # This is for checking diff in events that can also contain different applications
        if current_event_type != prev_event_type or current_active_window_details != active_window_details:
            # if application is same but event is different, the name will be None
            current_active_window_name = parse_window_name_from_details(current_active_window_details)
            if current_active_window_name is not None:
                inactive_windows = active_windows.copy()
                if current_active_window_name in inactive_windows:
                    inactive_windows.remove(current_active_window_name)
                json_log = {
                    "trigger": 'mouse' if current_event_type == 1 else 'keyboard',
                    "active_window": {
                        'name': current_active_window_name,
                        'title': current_active_window_details
                    },
                    "inactive_windows": inactive_windows,
                    "timestamp": datetime.utcnow().isoformat(),
                    "bitmap": ''
                }
                print("CURRENT ACTIVE WINDOW IS")
                print(current_active_window_name)
                if log_event(json_log):
                    print('Successfully logged event')
                else:
                    print('Unsuccessfully logged event')
                if len(current_active_window_details) > 0:
                    logging.info(json_log)

        active_window_details = current_active_window_details
        prev_event_type = current_event_type


def set_event_type(event_type_input):
    global current_event_type
    global last_time

    current_event_type = event_types[event_type_input]
    if datetime.utcnow() - last_time >= timedelta(seconds=2):
        # log_window_details()
        payload = active_window_process()
        if payload is not None:
            payload['event_type'] = event_type_input
            log_event(payload)
        log_processes(all_open_windows())
        last_time = datetime.utcnow()


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


def get_PID(window_string):
    first_chars = window_string[0:72]
    split_window_name = first_chars.split(' ')
    process_id = split_window_name[len(split_window_name) - 1]
    return process_id


def get_image_from_path(path, process_id):
    if path == "Error: No path found":
        return

    path = path.replace("\\", "/")
    try:
        icoX = win32api.GetSystemMetrics(win32con.SM_CXICON)
        icoY = win32api.GetSystemMetrics(win32con.SM_CXICON)

        large, small = win32gui.ExtractIconEx(path, 0)
        win32gui.DestroyIcon(small[0])

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, icoX, icoX)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        from PIL import Image
        bmp_str = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmp_str, 'raw', 'BGRA', 0, 1
        )
        img.save(process_id + '.png')
    except:  # Function will fail at 'hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))' due to end of list error
        pass


def export_bitmap_current_window():  # Returns bytes which can be stored in the JSON
    import win32gui
    import win32ui
    import win32con
    from PIL import Image
    import numpy
    import cv2
    import pickle
    hwnd = win32gui.GetForegroundWindow()
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()  # Creates bitmap of current active window

    _left, _top, _right, _bottom = win32gui.GetWindowRect(hwnd)
    w = _right - _left
    h = _bottom - _top

    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
    # dataBitMap.SaveBitmapFile(cDC, cur_time+".bmp") #Saves the bitmap image
    bmp_info = dataBitMap.GetInfo()
    bmp_array = numpy.asarray(dataBitMap.GetBitmapBits(), dtype=numpy.uint8)
    pil_im = Image.frombuffer('RGB', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_array, 'raw', 'RGBX', 0, 1)
    pil_array = numpy.array(pil_im)
    cv_im = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)  # Converts bitmap to ndarray
    bitmap_pickle = pickle.dumps(cv_im)  # Converts ndarray to bytes
    # Free Resources, this step is required
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return bitmap_pickle  # Returns bytes which we can store


def read_bitmap_image(bitmap_pickle):  # Takes in bytes
    from PIL import Image
    import pickle
    ndarray = pickle.loads(bitmap_pickle)  # Converts bytes back to ndarray
    im = Image.fromarray(ndarray).convert(
        'RGB')  # Converts ndarray to a PIL image, which can be saved with any file extension
    # cur_time = datetime.utcnow().isoformat()
    # cur_time = cur_time.replace(":", "'-'")
    # im.save("bob.bmp")
    return im  # Returns image object


def on_press(key):
    # t = Thread(target=set_event_type, args=(KEYBOARD_PRESS,))
    # t.start()
    set_event_type(KEYBOARD_PRESS)
    print("ON PRESS:", datetime.utcnow())
    # log_event(active_window_process())
    # logging.info("Key Press: " + str(key))
    # print("Key Press: " + str(key))


def on_release(key):
    # t = Thread(target=set_event_type, args=(KEYBOARD_RELEASE,))
    # t.start()
    set_event_type(KEYBOARD_RELEASE)
    print("ON RELEASE:", datetime.utcnow())
    # logging.info("Key Press: " + str(key))
    # print("Key Press: " + str(key))


def on_move(x, y):
    pass
    # t = Thread(target=set_event_type, args=(MOUSE_MOVE,))
    # t.start()
    set_event_type(MOUSE_MOVE)
    print("ON MOVE:", datetime.utcnow())
    # TODO: Limit this to maybe one trigger per second; no reason for 100+ logged events per second
    # log_event(active_window_process())
    # time.sleep(5)
    # logging.info("Mouse moved to ({0}, {1})".format(x, y))
    # print("Mouse moved to ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    if pressed:
        # t = Thread(target=set_event_type, args=(MOUSE_CLICK,))
        # t.start()
        set_event_type(MOUSE_CLICK)
        print("ON CLICK:", datetime.utcnow())
        # log_event(active_window_process())
        # logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        # print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))


def on_scroll(x, y, dx, dy):
    # t = Thread(target=set_event_type, args=(MOUSE_SCROLL,))
    # t.start()
    set_event_type(MOUSE_SCROLL)
    print("ON SCROLL:", datetime.utcnow())
    # log_event(active_window_process())
    # logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


def start_listeners():
    with MouseListener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as m_listener:
        with KeyboardListener(on_press=on_press, on_release=on_release) as k_listener:
            m_listener.join()
            k_listener.join()


if __name__ == '__main__':
    start_listeners()
