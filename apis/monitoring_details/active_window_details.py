#!/usr/bin/env python

"""Find the currently active window."""
# https://inneka.com/programming/python/obtain-active-window-using-python/

import logging
import subprocess
import sys


def get_open_windows_in_task_manager():
    open_apps = []
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            if not line.decode()[0].isspace():
                app_name = line.decode().rstrip()
                # print(app_name)
                open_apps.append(app_name)
    return open_apps

def get_path_from_pid(process_ID):
    #cmd = 'Get-CimInstance Win32_Process -Filter "ProcessID=3616" | Select-Object ProcessId, CommandLine'
    #'Get-CimInstance' command not working
    cmd = 'wmic process get processid,commandline'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            input_string = line.decode().rstrip()
            split_window_name = input_string.split(' ')
            in_process_ID = split_window_name[len(split_window_name) - 1]
            if in_process_ID == process_ID:
                pathname = input_string.split('\"')
                if len(pathname) > 1:
                    #print(pathname[1]) #Prints path
                    return pathname[1]
    return "Error: No path found"

def get_active_window():
    """
    Get the currently active window.

    Returns
    -------
    string :
        Name of the currently active window.
    """
    import sys
    active_window_name = None
    if sys.platform in ['linux', 'linux2']:
        # Alternatives: http://unix.stackexchange.com/q/38867/4784
        try:
            import wnck
        except ImportError:
            logging.info("wnck not installed")
            wnck = None
        if wnck is not None:
            screen = wnck.screen_get_default()
            screen.force_update()
            window = screen.get_active_window()
            if window is not None:
                pid = window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    active_window_name = f.read()
        else:
            try:
                from gi.repository import Gtk, Wnck
                gi = "Installed"
            except ImportError:
                logging.info("gi.repository not installed")
                gi = None
            if gi is not None:
                Gtk.init([])  # necessary if not using a Gtk.main() loop
                screen = Wnck.Screen.get_default()
                screen.force_update()  # recommended per Wnck documentation
                active_window = screen.get_active_window()
                pid = active_window.get_pid()
                with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                    active_window_name = f.read()
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        # http://stackoverflow.com/a/608814/562769
        import win32gui
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        # http://stackoverflow.com/a/373310/562769
        from AppKit import NSWorkspace
        active_window_name = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is unknown. Please report."
              .format(platform=sys.platform))
        print(sys.version)
    return active_window_name


if __name__ == '__main__':
    print("Active window: %s" % str(get_active_window()))
    get_open_windows_in_task_manager()
