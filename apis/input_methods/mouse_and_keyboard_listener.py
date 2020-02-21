import logging
import sys
import time
from datetime import datetime

from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

from apis.monitoring_details.active_window_details import get_active_window, get_open_windows_in_task_manager

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
            open_windows = []
            # On windows we want to use window name from task manager, but on mac we only have current window name
            if sys.platform in ['Windows', 'win32', 'cygwin']:
                open_windows = get_open_windows_in_task_manager()
                if len(open_windows) > 2:
                    open_windows = open_windows[2:]
            else:
                # On windows current_details is a lot more in depth, on mac its just the app name
                open_windows.append(current_active_window_details)
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
            # Adds any new windows to the list
            for w in range(len(open_windows)):
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

        # This is for checking diff in events that can also contain different applications
        if current_event_type != prev_event_type or current_active_window_details != active_window_details:
            # if application is same but event is different, the name will be None
            current_active_window_name = parse_window_name_from_details(current_active_window_details)
            if current_active_window_name is not None:
                json_log = {
                    "Event Type": current_event_type,
                    "Window Name": current_active_window_name,
                    "Window Details": current_active_window_details,
                    "Time Stamp": datetime.now().isoformat(),
                }
                if len(current_active_window_details) > 0:
                    logging.info(json_log)

        active_window_details = current_active_window_details
        prev_event_type = current_event_type


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


def set_event_type(event_type_input):
    global current_event_type
    current_event_type = event_types[event_type_input]
    log_window_details()


def on_press(key):
    set_event_type(KEYBOARD_PRESS)
    # print("ON PRESS")
    # logging.info("Key Press: " + str(key))
    # print("Key Press: " + str(key))


def on_release(key):
    set_event_type(KEYBOARD_RELEASE)
    # print("ON PRESS")
    # logging.info("Key Press: " + str(key))
    # print("Key Press: " + str(key))


def on_move(x, y):
    set_event_type(MOUSE_MOVE)
    # print("ON MOVE")
    # logging.info("Mouse moved to ({0}, {1})".format(x, y))
    # print("Mouse moved to ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    if pressed:
        set_event_type(MOUSE_CLICK)
        # print("ON CLICK")
        # logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        # print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))


def on_scroll(x, y, dx, dy):
    set_event_type(MOUSE_SCROLL)
    # print("ON SCOLL")
    # logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


with MouseListener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as m_listener:
    with KeyboardListener(on_press=on_press, on_release=on_release) as k_listener:
        m_listener.join()
        k_listener.join()
