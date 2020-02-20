import logging
import sys
import time

from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

from apis.monitoring_details.active_window_details import get_active_window, get_open_windows_in_task_manager

logging.basicConfig(filename="../window_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

MOUSE = "MOUSE"
KEYBOARD = "KEYBOARD"

event_types = {
    KEYBOARD: 0,
    MOUSE: 1,
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
            else:
                # On windows current_details is a lot more in depth, on mac its just the app name
                open_windows.append(current_active_window_details)
            # Logs all windows that have been closed
            for active_window in active_windows:
                if active_window not in open_windows:
                    # print(active_window + " is no longer open")
                    logging.info(active_window + " is no longer open")
            # Adds any new windows to the list
            for window in open_windows:
                if window not in active_windows:
                    # print(window + " is now added to the list of open windows")
                    active_windows.append(window)
                    logging.info(window + " is now added to the list of open windows")

            # On windows try to match this to closest name on open task manager apps
            # On mac leave as is
            current_active_window_name = current_active_window_details

        # This is for checking diff in events that can also contain different applications
        if current_event_type != prev_event_type or current_active_window_details != active_window_details:
            # if application is same but event is different, the name will be None
            if current_active_window_name is None:
                current_active_window_name = current_active_window_details
            print("Event type " + str(
                current_event_type) + "{V}" + "Window Name " + current_active_window_name + "{V}" + "Window details " +
                  str(current_active_window_details))
            logging.info("Event type " + str(
                current_event_type) + "{V}" + "Window Name " + current_active_window_name + "{V}" + "Window details " +
                         str(current_active_window_details))

        active_window_details = current_active_window_details
        prev_event_type = current_event_type


def set_event_type(event_type_input):
    global current_event_type
    current_event_type = event_types[event_type_input]
    log_window_details()


def on_press(key):
    set_event_type(KEYBOARD)
    # print("ON PRESS")
    # logging.info("Key Press: " + str(key))
    # print("Key Press: " + str(key))


def on_move(x, y):
    set_event_type(MOUSE)
    # print("ON MOVE")
    # logging.info("Mouse moved to ({0}, {1})".format(x, y))
    # print("Mouse moved to ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    if pressed:
        set_event_type(MOUSE)
        # print("ON CLICK")
        # logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        # print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))


def on_scroll(x, y, dx, dy):
    set_event_type(MOUSE)
    # print("ON SCOLL")
    # logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


with MouseListener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as m_listener:
    with KeyboardListener(on_press=on_press) as k_listener:
        m_listener.join()
        k_listener.join()
