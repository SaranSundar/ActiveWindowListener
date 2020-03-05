import logging
import sys
import time
from datetime import datetime

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


if __name__ == '__main__':
    while True:
        log_window_details()
        time.sleep(0.5)
