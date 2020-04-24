import json
from datetime import datetime, timedelta, date, time

import pytz
from flask import Blueprint

from apis.mongo.mongo_analytics import bpt_diagram_info, react_ui_info

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
        response = get_data_for_ui()
        socket.send(response)
        print("Sent", message)


def beginning_of_today():
    """
    Constructs a datetime for the current calendar date at 6:00AM.
    :return: a datetime instance for today at 6:00AM.
    """

    # TODO: Find timezone automatically
    tz = pytz.timezone("America/Chicago")
    # Find timestamp for today's date at 12:00:00 AM
    midnight_without_tz = datetime.combine(date.today(), time())
    yesterday_midnight_utc = tz.localize(midnight_without_tz).astimezone(pytz.utc)
    # Convert back to offset-naive timestamps for compatibility
    yesterday_midnight_utc = yesterday_midnight_utc.replace(tzinfo=None)
    # Return the time for 6am
    return yesterday_midnight_utc + timedelta(hours=6)


def get_data_for_ui():
    """
    Produces a JSONified version of analytics needed for ReactJS UI component.
    :return: a dict of necessary process information
    """

    timestamp = beginning_of_today()
    # Call analytics between 6am-8pm with active/idle/thinking timeouts
    return json.dumps(react_ui_info(timestamp, timestamp + timedelta(hours=14),
                                    5, 15, 60), default=str)


def get_analysis():
    """
    Produces a JSONified version of analytics needed for business process template
    swim lane diagram generation.
    :return: a dict of a process activity schedule
    """

    timestamp = beginning_of_today()
    # Call analytics between 6am-8pm with active/idle/thinking timeouts
    return json.dumps(bpt_diagram_info(timestamp, timestamp + timedelta(hours=14),
                                       5, 15, 60), default=str)


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
    pass
