import datetime

import pymongo

from apis.mongo.mongo_server import start_server, close_server

_DATABASE_NAME = 'timesheet'
_database_handle = None
_client_connection = None


def open_client(port=27017, timeout=30000):
    """
    Creates a MongoDB client connected to a MongoDB server.

    :param port: The port number of the intended MongoDB server. Defaults to 27017.
    :param timeout: The maximum amount of time before terminating connection attempts. Default to 30,000ms.
    :return: The MongoDB client object instance.
    :raise: An Exception if the client cannot connect.
    """

    global _database_handle
    global _client_connection

    # If client was not already made
    if not _client_connection:
        # Attempt a client connection
        _client_connection = client = pymongo.MongoClient('localhost', port, serverSelectionTimeoutMS=timeout)

        try:
            # Causes this thread to block until client has connected or not
            client.server_info()
            # Get handle on the database to be used
            _database_handle = client[_DATABASE_NAME]
            # Return client instance
            return client
        except Exception as e:
            # Raise exception if client cannot connect
            raise e

    # Client instance already created
    else:
        return _client_connection


def close_client():
    """
    Closes the MongoDB client.

    Formally disconnected the client. The client instance can be retrieved
    via open_client(). Issuing commands through it will automatically reopen it.
    :return: None
    :raise: An Exception if the client was never created or opened.
    """
    if _client_connection:
        _client_connection.close()
    else:
        raise Exception('no existing or open client to close')


def log_event(event: dict):
    """
    Writes the given event to the MongoDB server.

    Saves the provided event as a document under a collection named with
    today's date in ISO-8601 format. This collection is stored under a
    database within MongoDB with the name of _DATABASE_NAME.

    :param event: The dictionary containing data to write.
    :return: a MongoDB document object ID for the inserted event record
    :raise: An Exception if the client cannot connect or the event is not a dict
    """

    # Raise exception if invalid event object is given
    if type(event) is not dict:
        raise Exception('event must be of type dict.')

    # extract date from time
    date = event['timestamp'].split('T')[0]

    # obtain handle on collection for the day
    collection_handle = _database_handle[date]
    # Insert the event as a document in the collection; return its ID
    return collection_handle.insert_one(event).inserted_id


def get_database(database: str):
    return open_client()[database]


def get_collection(collection: str, database: str):
    return open_client()[database][collection]


if __name__ == '__main__':
    start_server()
    open_client(timeout=3000)
    print('Inserted object with ID ' + str(log_event({
        'time': datetime.datetime.today().isoformat(),
        'active': 'placeholder',
        'bitmap': 'placeholder',
        'idle': ['placeholder'],
        'trigger': {
            'reason': 'placeholder',
            'field': 'placeholder'
        }
    })))
    close_client()
    close_server()
else:
    print('Starting MongoDB server...')
    start_server()
    print('Opening MongoDB client...')
    open_client()
    print('Client connected.')
