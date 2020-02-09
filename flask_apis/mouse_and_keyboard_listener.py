import logging

from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

logging.basicConfig(filename="m_and_k.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')


def end_rec(key):
    # logging.info(str(key))
    print(str(key))


def on_press(key):
    # logging.info(str(key))
    print("Key Press: " + str(key))


def on_move(x, y):
    # logging.info("Mouse moved to ({0}, {1})".format(x, y))
    print("Mouse moved to ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    if pressed:
        # logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))


def on_scroll(x, y, dx, dy):
    # logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


with MouseListener(on_click=on_click) as m_listener:
    with KeyboardListener(on_press=on_press) as k_listener:
        m_listener.join()
        k_listener.join()
