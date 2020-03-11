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


def all_open_windows(with_title=True, blacklist: list or set = None, whitelist: list or set = None):
    """
    Returns information regarding all processes containing an
    open window on the system.

    Information is delivered on a per-PID basis, with open windows
    associated via their window handles and window titles. Process
    information is also provided in the process' PID, name, executable
    path, and owner's username.

    Individual processes can be blacklisted via their executable file paths,
    preventing matching processes from monitoring. Directories can be
    blacklisted as well, in which case the entirety of its contents and
    any subdirectories is blacklisted as well.

    Exceptions to the blacklist mentioned above can be given in the whitelist.
    Processes can be specified via their specific executable file paths or a
    directory under which they appear, as with the blacklist.

    :param with_title: Boolean indicating whether windows without titles should be ignored.
    :param blacklist: A list of processes or process directories to ignore
    :param whitelist: A list of processes or process directories to include despite blacklist
    :return: A dict of the described information
    """

    # Add additional blacklisted processes/directories if defined
    exe_blacklist = {'C:\\Windows', 'C:\\Program Files\\WindowsApps'}
    if blacklist:
        blacklist = set(blacklist) if isinstance(blacklist, list) else blacklist
        exe_blacklist = set.union(exe_blacklist, blacklist)

    # Add additional whitelisted processes/directories if defined
    exe_whitelist = {'C:\\Windows\\explorer.exe'}
    if whitelist:
        whitelist = set(whitelist) if isinstance(whitelist, list) else whitelist
        exe_whitelist = set.union(exe_whitelist, whitelist)

    # Obtain all windows' PIDs, HWNDs, and titles
    open_windows = _get_all_open_windows(with_title=with_title)
    # Pair PIDs with their processes and all discrete windows
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
        # Get process executable path
        process_exe = os.path.realpath(processes[pid]['process_obj']['exe'])
        # Check if it is included in the blacklist
        if any(os.path.commonprefix([process_exe, exe]) == exe for exe in exe_blacklist):
            # If in blacklist, check if not whitelisted
            if not any(os.path.commonprefix([process_exe, exe]) == exe for exe in exe_whitelist):
                # Blacklisted and not whitelisted? Then this process can be ignored from detection
                del processes[pid]

    return processes


def computer_snapshot(with_title=True, blacklist: list or set = None, whitelist: list or set = None):
    """
    Convenience function that returns information for both the
    currently active window and all open windows.

    Additionally adds the timestamp at which this information was taken.
    :param with_title: Boolean indicating whether windows without titles should be ignored.
    :param blacklist: A list of processes or process directories to ignore
    :param whitelist: A list of processes or process directories to include despite blacklist
    :return: A dict for the information above.
    """

    try:
        return {
            'active': active_window_process(),
            'all': all_open_windows(with_title=with_title, blacklist=blacklist, whitelist=whitelist),
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
