import subprocess
import sys

# Determine whether to use Windows CLI / PowerShell commands or *nix commands
_windows = sys.platform in ['Windows', 'win32', 'cygwin']
# Find location of MongoDB daemon process
_daemon_path = subprocess.check_output(['where' if _windows else 'which', 'mongod']).decode().strip()
# Define location of configuration file
_config_file = './mongoServer.config'
# Current handle server instance's process
_server = None


def start_server():
    """
    Creates a new process for a local MongoDB server. Does nothing if
    the process exists (the server is already active).
    :return: None
    """

    global _server
    if not _server:
        _server = subprocess.Popen([_daemon_path, '--config', _config_file], text=True)


def close_server():
    """
    Terminates the current process of the local MongoDB server. Does nothing if
    the process does not exist (the server is already inactive).
    :return: None
    """

    global _server
    if _server:
        _server.terminate()
        _server.wait()
        _server = None


if __name__ == '__main__':
    start_server()
    while input('Press q to quit: ') != 'q':
        pass
    close_server()
