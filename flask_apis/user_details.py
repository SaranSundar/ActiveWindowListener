import getpass
import os.path
import platform
import socket


def get_user_details():
    username = getpass.getuser()
    print("Username: " + username)

    homedir = os.path.expanduser("~")
    print("Home Directory: " + homedir)

    hostname = socket.gethostname()
    print("Hostname: " + hostname)

    althomedir = platform.node()
    print("Alt Hostname: " + althomedir)

    hostnamebyaddr = socket.gethostbyaddr(socket.gethostname())[0]
    print("Hostname by Address: " + hostnamebyaddr)


if __name__ == '__main__':
    get_user_details()
