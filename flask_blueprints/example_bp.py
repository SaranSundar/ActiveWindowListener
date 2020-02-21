import json

from flask import Blueprint

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
        response = json.dumps(message, default=str)
        response = {
            "Chrome": {"mouse_usage": 40, "keyboard_usage": 30, "idle": 10, "thinking": 20},
            "Visual Studio": {"mouse_usage": 20, "keyboard_usage": 50, "idle": 10, "thinking": 20}
            }
        socket.send(response)
        print("Sent", message)


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
