import json
from datetime import datetime, timedelta

from flask import Blueprint

from apis.mongo.mongo_analytics import bpt_diagram_info, react_ui_info
from apis.mongo.mongo_server import close_server

example_bp = Blueprint('example_bp', __name__)
example_ws = Blueprint('example_ws', __name__)


@example_ws.route("/echo-example")
def echo_example(socket):
    # Example usage of web socket to receive and send messages
    while not socket.closed:
        message = socket.receive()
        if message is None:
            continue
        message = json.loads(message)
        print("Received", message)
        # response = json.dumps(message, default=str)
        response = {
            "Google Chrome": {"mouse_usage": 40, "keyboard_usage": 30, "idle": 10, "thinking": 20},
            "Visual Studio": {"mouse_usage": 20, "keyboard_usage": 50, "idle": 10, "thinking": 20}
        }
        response = json.dumps(response, default=str)
        socket.send(response)
        print("Sent", message)


def get_data_for_ui():
    return react_ui_info(datetime.today() - timedelta(days=10),
                         datetime.today() + timedelta(days=1),
                         5, 15, 60)


def get_analysis():
    return bpt_diagram_info(datetime.today() - timedelta(days=10),
                            datetime.today() + timedelta(days=1),
                            5, 15, 60)


@example_bp.route("/get-long-example")
def get_long_example():
    # Imports long method from api file to keep bp file clean and simple
    pass


@example_bp.route("/get-example/<parameter>")
def get_example(parameter):
    # Example GET request to be called with parameter
    status = {"status": "Success"}
    status = json.dumps(status)
    return status


if __name__ == '__main__':
    from pprint import pprint

    pprint(get_data_for_ui())
    print("\n")
    pprint(get_analysis())
    close_server()
