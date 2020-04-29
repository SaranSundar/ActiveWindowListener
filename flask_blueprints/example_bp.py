import json
from datetime import datetime, timedelta, date, time

import pytz
from flask import Blueprint

from apis.input_methods.diagram import generateDiagram
from apis.mongo.mongo_analytics import bpt_diagram_info, react_ui_info
from apis.monitoring_details.user_network_details import get_user_details

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
        # response = json.dumps(message, default=str)
        socket.send(response)
        print("Sent", message)


def time_from_beginning_of_today(offset: timedelta = None):
    """
    Constructs a datetime for the current calendar date with an optional offset
    from 12:00AM.
    :return: a datetime instance for the indicated time
    """

    # TODO: Find timezone automatically
    tz = pytz.timezone("America/Chicago")
    # Find timestamp for today's date at 12:00:00 AM
    midnight_without_tz = datetime.combine(date.today(), time())
    yesterday_midnight_utc = tz.localize(midnight_without_tz).astimezone(pytz.utc)
    # Convert back to offset-naive timestamps for compatibility
    yesterday_midnight_utc = yesterday_midnight_utc.replace(tzinfo=None)
    # Account for requested offset
    return yesterday_midnight_utc + offset if offset is not None else timedelta(seconds=0)


def get_data_for_ui():
    """
    Produces a JSONified version of analytics needed for ReactJS UI component.
    :return: a dict of necessary process information
    """

    start = time_from_beginning_of_today(offset=timedelta(hours=0))  # 6:00AM
    end = time_from_beginning_of_today(offset=timedelta(hours=24))  # 11:59PM
    # Call analytics between 6am-8pm with active/idle/thinking timeouts
    return json.dumps(react_ui_info(start, end, 5, 15, 60), default=str)


def get_analysis():
    """
    Produces a JSONified version of analytics needed for business process template
    swim lane diagram generation.
    :return: a dict of a process activity schedule
    """

    start = time_from_beginning_of_today(offset=timedelta(hours=6))  # 6:00AM
    end = time_from_beginning_of_today(offset=timedelta(hours=24))  # 11:59PM
    # Call analytics between 6am-8pm with active/idle/thinking timeouts
    return json.dumps(bpt_diagram_info(start, end, 5, 15, 60), default=str)


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
    generateDiagram(get_analysis(), get_user_details())
