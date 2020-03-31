from datetime import datetime, timedelta

from apis.mongo.mongo_client import EVENT_DATABASE_NAME, WINDOWS_DATABASE_NAME, get_collection
from apis.mongo.mongo_server import close_server


def read_events(start: datetime, end: datetime):
    """
    Obtains all events logged in MongoDB between the start and end time given, inclusive.
    :param start: a datetime instance in UTC time
    :param end: a datetime instance in UTC time
    :return: a List of MongoDB event documents
    """

    # Base case: no valid range given
    if end <= start:
        return []

    # Base case: start date is after current time
    if start >= datetime.utcnow():
        return []

    events = []
    # Get events for start date, where time needs to be considered
    events += get_collection(EVENT_DATABASE_NAME, str(start.date())).find({'timestamp': {'$gte': start}})
    # Get events for all intermediate dates
    start += timedelta(days=1)
    while start.date() < end.date():
        # print(start.date())
        events += get_collection(EVENT_DATABASE_NAME, str(start.date())).find({})
        start += timedelta(days=1)
    # Get events for end date, where time needs to be considered
    events += get_collection(EVENT_DATABASE_NAME, str(start.date())).find({'timestamp': {'$lte': end}})

    return events


def read_processes(start: datetime, end: datetime):
    """
    Obtains all process snapshots logged in MongoDB between the start and end time given, inclusive.
    :param start: a datetime instance in UTC time
    :param end: a datetime instance in UTC time
    :return: a List of MongoDB process logs
    """

    # Base case: no valid range given
    if end <= start:
        return []

    # Base case: start date is after current time
    if start >= datetime.utcnow():
        return []

    processes = []
    # Get processes for start date, where time needs to be considered
    processes += get_collection(WINDOWS_DATABASE_NAME, str(start.date())).find({'timestamp': {'$gte': start}})
    # Get processes for all intermediate dates
    start += timedelta(days=1)
    while start.date() < end.date():
        # print(start.date())
        processes += get_collection(WINDOWS_DATABASE_NAME, str(start.date())).find({})
        start += timedelta(days=1)
    # Get processes for end date, where time needs to be considered
    processes += get_collection(WINDOWS_DATABASE_NAME, str(start.date())).find({'timestamp': {'$lte': end}})

    return processes


def process_events(events: list, active_buffer: int = 5, idle_buffer: int = 300, thinking_buffer: int = 900):
    window_events_times = {}

    for event in events:
        # Start tracking this window
        if event['window_name'] not in window_events_times:
            window_events_times[event['window_name']] = []

        # Append tuple (time, event type) for the window
        window_events_times[event['window_name']].append((
            datetime.fromisoformat(event['timestamp']), event['event_type']
        ))

    window_stats = {}
    for window in window_events_times:
        window_stats[window] = times = {'mouse': [], 'kb': [], 'active': [], 'idle': [], 'thinking': []}
        for instance in window_events_times[window]:
            # determine which event this was
            category = 'kb' if instance[1] == 0 else 'mouse'
            # no events recorded
            if len(times[category]) == 0:
                times[category].append((instance[0], instance[0]))
            # new event is over active_buffer later than prev event
            elif instance[0] - times[category][-1][1] > timedelta(seconds=active_buffer):
                times[category].append((instance[0], instance[0]))
            # new event is under/equal active_buffer later than prev event
            elif instance[0] - times[category][-1][1] <= timedelta(seconds=active_buffer):
                # Extend last interval to current time
                last_int = times[category][-1]
                times[category][-1] = (last_int[0], instance[0])

    for window in window_stats:
        # compile all events for that window
        window_stats[window]['all'] = all_events = sorted(window_stats[window]['kb'] + window_stats[window]['mouse'])
        working_interval = [all_events[0][0], all_events[0][1]]
        for event in all_events:
            # each tuple is (start, end) for mouse/kb events respectively

            # mouse/kb time interval overlaps with existing interval
            if event[0] <= working_interval[1]:
                working_interval[1] = event[1]
            # mouse/kb time interval is within active_buffer of last end time
            elif event[0] - working_interval[1] <= timedelta(seconds=active_buffer):
                working_interval[1] = event[1]
            # mouse/kb time interval is within idle_buffer of last end time
            elif event[0] - working_interval[1] <= timedelta(seconds=idle_buffer):
                window_stats[window]['active'].append(tuple(working_interval))  # track active time interval
                window_stats[window]['idle'].append((working_interval[1], event[0]))  # track idle time interval
                working_interval = [event[0], event[1]]  # reset working interval
            # mouse/kb time interval is within thinking_buffer of last end time
            elif event[0] - working_interval[1] <= timedelta(seconds=thinking_buffer):
                window_stats[window]['active'].append(tuple(working_interval))  # track active time interval
                window_stats[window]['thinking'].append((working_interval[1], event[0]))  # track thinking time interval
                working_interval = [event[0], event[1]]  # reset working interval
            # mouse/kb time interval is exceeds thinking buffer => assume window closed
            else:
                working_interval = [event[0], event[1]]

    for window in window_stats:
        totals = window_stats[window]['totals'] = dict()
        totals['mouse'] = sum([interval[1] - interval[0] for interval in window_stats[window]['mouse']],
                              timedelta())
        totals['kb'] = sum([interval[1] - interval[0] for interval in window_stats[window]['kb']], timedelta())
        totals['active'] = sum([interval[1] - interval[0] for interval in window_stats[window]['active']],
                               timedelta())
        totals['idle'] = sum([interval[1] - interval[0] for interval in window_stats[window]['idle']],
                             timedelta())
        totals['thinking'] = sum([interval[1] - interval[0] for interval in window_stats[window]['thinking']],
                                 timedelta())
        totals['not_closed'] = sum([totals[cat] for cat in ['active', 'idle', 'thinking']], timedelta())

    stats = {
        window:
            {
                'active': window_stats[window]['totals']['active'] / window_stats[window]['totals']['not_closed'] * 100,
                'idle': window_stats[window]['totals']['idle'] / window_stats[window]['totals']['not_closed'] * 100,
                'thinking': window_stats[window]['totals']['thinking'] / window_stats[window]['totals'][
                    'not_closed'] * 100,
                'mouse_usage': window_stats[window]['totals']['mouse'] / window_stats[window]['totals']['active'] * 100,
                'keyboard_usage': window_stats[window]['totals']['kb'] / window_stats[window]['totals']['active'] * 100
            }
        for window in window_stats
    }

    return stats


def stats_between_times(start: str, end: str, active_buf: int = 5, idle_buf: int = 300, thinking_buf: int = 900):
    """
   Obtains all events logged in MongoDB between the start and end time given, inclusive.
   :param start: an ISO-8601 string in UTC time
   :param end: an ISO-8601 string in UTC time
   :param active_buf: number of seconds defining maximum window of inactivity still counted as "active" time
   :param idle_buf: number of seconds defining maximum window of inactivity still counted as "idle" time
   :param thinking_buf: number of seconds defining maximum window of inactivity still counted as "thinking" time
   :return: a dict with stats for each window in the time span
   """
    events = read_events(start, end)
    stats = process_events(events, active_buf, idle_buf, thinking_buf)
    return stats


def business_process_info(start: datetime, end: datetime, active_buf: int, idle_buf: int, think_buf: int):
    user_events = read_events(start, end)  # Tells us what the active process/window is
    window_log = read_processes(start, end)  # Tells us what all processes/windows are
    intervals = {}  # TODO: use a custom dict that auto-initializes nonexistent entries?

    # Iterate through events in order of timestamps
    user_event_index, window_log_index = 0, 0
    while user_event_index < len(user_events) and window_log_index < len(window_log):
        if user_events[user_event_index]['timestamp'] <= window_log[window_log_index]['timestamp']:
            # TODO: process user event w/ active window
            user_event_index += 1
        else:
            # TODO: process window log event w/ open window information
            window_log_index += 1
    # Iterate through remaining of user events
    while user_event_index < len(user_events):
        # TODO: process user event w/ active window
        user_event_index += 1
    # Iterate through remaining of window log events
    while window_log_index < len(window_log):
        # TODO: process window log event w/ open window information
        window_log_index += 1

    # Finalize all events and determine stats
    [interval.finalize() for interval in intervals]

    # Return results of analysis in the time range provided
    # TODO: What exactly to return
    return None


if __name__ == '__main__':
    # now = datetime.utcnow() - timedelta(days=10)
    # tmrw = datetime.utcnow()
    # print(read_events(now.isoformat(), tmrw.isoformat()))
    business_process_info(datetime.utcnow() - timedelta(days=30), datetime.utcnow() - timedelta(days=1), 5, 5, 5)
    close_server()
    pass
