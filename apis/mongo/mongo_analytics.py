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
    events += database[str(start.date())].find({'timestamp': {'$gte': start.isoformat()}})
    # Get events for all intermediate dates
    start += timedelta(days=1)
    while start.date() < end.date():
        print(start.date())
        events += database[str(start.date())].find({})
        start = start + timedelta(days=1)
    # Get events for end date, where time needs to be considered
    events += database[str(end.date())].find({'timestamp': {'$lte': end.isoformat()}})

    return events


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


if __name__ == '__main__':
    # now = datetime.utcnow() - timedelta(days=10)
    # tmrw = datetime.utcnow()
    # print(read_events(now.isoformat(), tmrw.isoformat()))
    pass
