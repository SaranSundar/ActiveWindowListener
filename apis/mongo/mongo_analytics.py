from datetime import datetime, timedelta

from apis.mongo.mongo_client import get_database


def read_events(start: str, end: str):
    """
    Obtains all events logged in MongoDB between the start and end time given, inclusive.
    :param start: an ISO-8601 string in UTC time
    :param end: an ISO-8601 string in UTC time
    :return: a List of MongoDB event documents
    """

    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)

    # Base case: no valid range given
    if end <= start:
        return []

    # Base case: start date is after current time
    if start > datetime.utcnow():
        return []

    # Database with all events stored under the the day they occurred on
    database = get_database('timesheet')

    events = []
    # Get events for start date, where time needs to be considered
    events += database[str(start.date())].find({'timestamp': {'$gte': start}})
    # Get events for all intermediate dates
    start = start + timedelta(days=1)
    while start.date() < end.date():
        print(start.date())
        events += database[str(start.date())].find({})
        start = start + timedelta(days=1)
    # Get events for end date, where time needs to be considered
    events += database[str(end.date())].find({'timestamp': {'$lte': end}})

    return events


if __name__ == '__main__':
    # now = datetime.utcnow() - timedelta(days=10)
    # tmrw = datetime.utcnow()
    # print(read_events(now.isoformat(), tmrw.isoformat()))
    pass
