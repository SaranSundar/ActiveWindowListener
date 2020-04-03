from datetime import timedelta


class ApplicationTimeLog:

    def __init__(self, active: int, idle: int, thinking: int):
        self.active_times = []  # During what times is this an active process
        self.idle_times = []  # During what times is this an idle process
        self.thinking_times = []  # During what times is this a thinking process
        self.open_times = []  # During what times is this process open at all
        self.timeouts = {'active': active, 'idle': idle, 'thinking': thinking}

        self.final_stats = {}

    def update_active(self, timestamp):
        # This application is being opened for the first time or has been closed already
        if len(self.open_times) == 0 or self.open_times[-1][1] is not None:
            self.open_times.append([timestamp, None])

        # If no active times are logged, start a new interval
        if len(self.active_times) == 0:
            self.active_times.append([timestamp, timestamp])
            return

        # Get the last interval
        last_interval = self.active_times[-1]
        # Determine if the last time this was active was within active timeout window
        if timestamp - last_interval[1] <= timedelta(seconds=self.timeouts['active']):
            # If so, extend the last interval recorded
            self.active_times[-1][1] = timestamp
            return
        else:
            # It's active now, so create a new active window
            self.active_times.append([timestamp, timestamp])

        # Check if within idle timeout window
        if timestamp - last_interval[1] <= timedelta(seconds=self.timeouts['idle']):
            # If so, create an interval originating from the last active time to now
            self.idle_times.append([self.active_times[-1][1], timestamp])
        # Check if within thinking timeout window
        elif timestamp - last_interval[1] <= timedelta(seconds=self.timeouts['thinking']):
            # If so, create an interval originating from the last active time to now
            self.thinking_times.append([self.active_times[-1][1], timestamp])
        # If it's been even longer, do something
        else:
            pass

    def update_is_open(self, timestamp):
        # If this app hasn't been open before
        if len(self.open_times) == 0:
            self.open_times.append([timestamp, None])
            return

        # If this app has been closed already
        if self.open_times[-1][1] is not None:
            self.open_times[-1][1] = timestamp

    def finalize(self):
        # Terminate open status if necessary
        if self.open_times[-1][1] is None:
            self.open_times[-1][1] = max(self.active_times[-1][1], self.idle_times[-1][1], self.thinking_times[-1][1])

        # Calculate total amounts of time among categories by summing intervals
        self.final_stats['active_time'] = sum(t2 - t1 for t1, t2 in self.active_times)
        self.final_stats['idle_time'] = sum(t2 - t1 for t1, t2 in self.idle_times)
        self.final_stats['thinking_time'] = sum(t2 - t1 for t1, t2 in self.thinking_times)
        self.final_stats['open_time'] = sum(t2 - t1 for t1, t2 in self.open_times)
        return self.final_stats
