import logging
import time

from pynput.mouse import Listener

from active_window_details import get_active_window

logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

active_window_name = ""

# For OSX you need to run python with sudo or it won't work fine.


# def on_move(x, y):
#     logging.info("Mouse moved to ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    global active_window_name
    if pressed:
        time.sleep(0.1)
        active_window_name = get_active_window()
        print(active_window_name)
        # logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))


# def on_scroll(x, y, dx, dy):
#     logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


with Listener(on_click=on_click) as listener:
    listener.join()
