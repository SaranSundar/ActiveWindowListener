import os
import time
from datetime import datetime
from pprint import pprint

import psutil
import win32gui
import win32process


def active_window_process():
    """
    Obtains information regarding the currently active window including the window's
    underlying process' PID, name, executable path, and owner's username. Also
    retrieves the window's handle and the title of the window,
    :return: The information described above as a dictionary.
    """

    # Get handle of active window
    hwnd = win32gui.GetForegroundWindow()
    # Get thread of active window and pid of process responsible for active window
    tid, pid = win32process.GetWindowThreadProcessId(hwnd)
    # Generate process object for the found pid
    proc = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'exe', 'username'])
    # Create a dictionary for the information found
    active = {'process_obj': proc, 'window': {'hwnd': hwnd, 'title': win32gui.GetWindowText(hwnd)}}
    return active


def _get_all_open_windows(with_title=True):
    """
    Returns a list of all windows open on the system with their process' PID,
    the window handle, and the title of the window.

    Automatically filters out all windows that do not have a title. This eliminates
    the majority of "windows" that are active on the system but do not actually show
    up as windows that the user can interact with. This behavior can be disabled.
    :param with_title: Boolean indicating whether windows without titles should be ignored.
    :return: A list of tuples for each window.
    """

    def callback(hwnd, array):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if with_title and title:
                tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                array.append((pid, hwnd, title))

    # list storing all windows in query
    windows = []
    # Calls callback function once per window, passing the window handle automatically
    win32gui.EnumWindows(callback, windows)
    return windows


def all_open_windows(with_title=True, blacklist: list or set = None):
    """
    Returns information regarding all processes containing an
    open window on the system.

    Information is delivered on a per-PID basis, with open windows
    associated via their window handles and window titles. Process
    information is also provided in the process' PID, name, executable
    path, and owner's username.
    :param blacklist: A list of processes or process directories to ignore
    :param with_title: Boolean indicating whether windows without titles should be ignored.
    :return: A dict of the described information
    """

    # Add additional blacklisted processes/directories if defined
    exe_blacklist = {'C:\\Windows', 'C:\\Program Files\\WindowsApps'}
    if blacklist:
        if type(blacklist) is list:
            blacklist = set(blacklist)
        exe_blacklist = set.union(exe_blacklist, blacklist)

    # Obtain all windows' PIDs, HWNDs, and titles
    open_windows = _get_all_open_windows(with_title=with_title)
    # Pair PIDs with processes and windows
    processes = {}
    for pid, hwnd, title in open_windows:
        if pid in processes:
            processes[pid]['windows'].append((hwnd, title))
        else:
            processes[pid] = {
                'process_obj': psutil.Process(pid=pid).as_dict(attrs=['pid', 'name', 'exe', 'username']),
                'windows': [{'hwnd': hwnd, 'title': title}]
            }

    # Remove any processes that match an entry in the blacklist
    for pid in list(processes.keys()):
        for exe in exe_blacklist:
            proc_exe = os.path.realpath(processes[pid]['process_obj']['exe'])
            if os.path.commonprefix([proc_exe, exe]) == exe:
                del processes[pid]
                break

    return processes


def computer_snapshot(with_title=True, blacklist: list or set = None):
    """
    Convenience function that returns information for both the
    currently active window and all open windows.

    Additionally adds the timestamp at which this information was taken.
    :param blacklist: A list of processes or process directories to ignore
    :param with_title: Boolean indicating whether windows without titles should be ignored.
    :return: A dict for the information above.
    """

    try:
        return {
            'active': active_window_process(),
            'all': all_open_windows(with_title=with_title, blacklist=blacklist),
            'timestamp': datetime.utcnow()
        }
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    while True:
        s = time.time()
        snapshot = computer_snapshot()
        if snapshot is None:
            continue
        print("Active: " + snapshot['active']['process_obj']['name'])
        for key, value in snapshot['all'].items():
            print("Window Title: " + value['process_obj']['name'])
        # pprint(snapshot)
        print('time taken: {}'.format(time.time() - s))
        print("")
