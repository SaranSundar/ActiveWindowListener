import platform
import time
from http.client import HTTPConnection
from threading import Thread

import webview
from apis.input_methods.mouse_and_keyboard_listener import start_listeners
from app import run_app

error = False
status = False
port = 43968

operating_system = str(platform.system()).lower()


def get_user_agent(window):
    result = window.evaluate_js(r"""
        // Return user agent
        'User agent:\n' + navigator.userAgent;
        """)
    print(result)


def is_server_running(url, max_wait):
    global error
    global status
    global port

    time.sleep(0.4)
    start = time.time()
    while True:
        try:
            end = time.time()
            if end - start > max_wait:
                return False
            time.sleep(0.1)
            connection = HTTPConnection(url, port)
            request, response = connection.request("GET", "/"), connection.getresponse()
            if response is not None:
                status = response.status
                return True
        except Exception as e:
            error = e
            print("Server not yet running")


def main():
    global port

    url, max_wait = 'localhost', 15  # 15 seconds
    link = "http://" + url + ":" + str(port)
    # Starting Server
    t = Thread(target=start_listeners, args=())
    t.daemon = True
    t.start()
    print("Listeners started")
    server_thread = Thread(target=run_app, args=(url, port))
    server_thread.daemon = True
    server_thread.start()
    # Waiting for server to load content
    if is_server_running(url, max_wait):
        print("Server started")
        # webbrowser.open(link, new=2)
        # while server_thread.is_alive():
        #     time.sleep(0.1)
        window = webview.create_window("Flair App", link, width=1000, height=522)
        # If you want to inspect element just go to localhost url in browser
        webview.start(get_user_agent, window, debug=True)
    else:
        print("Server failed to start with a max wait time of " + str(max_wait))
        if status is not False:
            print("Status was " + str(status))
        if error is not False:
            print("Exception was " + str(error))
    print("Server has exited")


if __name__ == '__main__':
    main()
