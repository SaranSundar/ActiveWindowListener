import heapq
from datetime import datetime, timedelta
from pprint import pprint

from apis.mongo.ApplicationTimeLog import ApplicationTimeLog
from apis.mongo.DefaultDict import DefaultDict
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


def business_process_info(start: datetime, end: datetime, active_buf: int, idle_buf: int, think_buf: int):
    user_events = read_events(start, end)  # Tells us what the active process/window is
    window_log = read_processes(start, end)  # Tells us what all processes/windows are
    intervals = DefaultDict(lambda: ApplicationTimeLog(active_buf, idle_buf, think_buf))

    # Iterate through events in order of timestamps
    user_event_index, window_log_index = 0, 0
    while user_event_index < len(user_events) and window_log_index < len(window_log):
        if user_events[user_event_index]['timestamp'] < window_log[window_log_index]['timestamp']:
            intervals[user_events[user_event_index]['process_obj']['name']].update_active(
                user_events[user_event_index]['timestamp'])
            user_event_index += 1
        else:
            curr_log = window_log[window_log_index]
            pids = [key for key in curr_log.keys() if key not in ['_id', 'timestamp']]
            open_apps = [curr_log[pid]['process_obj']['name'] for pid in pids]
            for app in intervals.as_dict():
                if app in open_apps:
                    intervals[app].update_is_open(curr_log['timestamp'])
                else:
                    intervals[app].update_is_closed(curr_log['timestamp'])
            window_log_index += 1

    # Iterate through remaining of user events
    while user_event_index < len(user_events):
        intervals[user_events[user_event_index]['process_obj']['name']].update_active(
            user_events[user_event_index]['timestamp'])
        user_event_index += 1

    # Iterate through remaining of window log events
    while window_log_index < len(window_log):
        curr_log = window_log[window_log_index]
        pids = [key for key in curr_log.keys() if key not in ['_id', 'timestamp']]
        open_apps = [curr_log[pid]['process_obj']['name'] for pid in pids]
        for app in intervals.as_dict():
            if app in open_apps:
                intervals[app].update_is_open(curr_log['timestamp'])
            else:
                intervals[app].update_is_closed(curr_log['timestamp'])
        window_log_index += 1

    # get results of analysis in the time range provided
    totals = {
        process: intervals[process].finalize()
        for process in intervals.as_dict().keys()
    }

    # generate "activities" list
    activities = []
    for process in intervals.as_dict().keys():
        activities += [(time, process) for time in intervals[process].open_times]

    schedule = schedule_activities(activities)
    schedule_dict = {}
    for row_num in range(len(schedule)):
        row = schedule_dict[f'list{row_num+1}'] = []
        for activity in schedule[row_num]:
            row.append({
                'name': activity[1],
                'start': activity[0][0].isoformat(),
                'finish': activity[0][1].isoformat(),
                'idle_time': intervals[activity[1]].total_idle_time(start, end)
            })
    return schedule_dict


def schedule_activities(activities):
    # sort activities by start time
    act_start = sorted(activities, key=lambda a: (a[0][0], a[0][1]))
    # sort activities by finish time
    act_finish = sorted(activities, key=lambda a: (a[0][1], a[0][0]))
    # generate list IDs in a heap
    lists = []
    num_lists = 0
    heapq.heapify(lists)
    # array pointers
    start, finish = 0, 0
    # list assignment map
    assignment = {}
    # storage list
    schedule = []

    while finish < len(act_finish):
        # finishing time needs to be processed
        if start >= len(act_start) or act_start[start][0][0] >= act_finish[finish][0][1]:
            # put the list occupied by the process back into the available lists
            heapq.heappush(lists, assignment[act_finish[finish][1]])
            # increment finish activity pointer
            finish += 1
        else:
            # no available lists
            if len(lists) == 0:
                # add a list
                num_lists += 1
                # add the list to queue
                heapq.heappush(lists, num_lists - 1)
            # Assign the list
            chosen_list = heapq.heappop(lists)
            assignment[act_start[start][1]] = chosen_list
            # add new list to schedule
            if chosen_list == len(schedule):
                schedule.append([])
            # add new item to existing list to schedule
            schedule[chosen_list].append(act_start[start])
            # increment start activity pointer
            start += 1

    return schedule


if __name__ == '__main__':
    # now = datetime.utcnow() - timedelta(days=10)
    # tmrw = datetime.utcnow()
    # print(read_events(now.isoformat(), tmrw.isoformat()))
    info = business_process_info(datetime.utcnow() - timedelta(days=10),
                                 datetime.utcnow() + timedelta(days=1),
                                 5, 15, 60)
    pprint(info)
    close_server()
    pass
