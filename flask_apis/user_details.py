import getpass
import os.path
import platform
import re
import socket
import uuid


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

    IPAddr = socket.gethostbyname(socket.gethostname())
    print("IP Address: " + IPAddr)

    MacAddr = hex(uuid.getnode())
    print("MAC Address: " + MacAddr)

    print("Formatted MAC address: ", end="")
    print(':'.join(re.findall('..', '%012x' % uuid.getnode())))


if __name__ == '__main__':
    get_user_details()
