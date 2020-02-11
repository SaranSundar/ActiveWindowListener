import getpass
import os.path
import platform
import re
import socket
import subprocess
import sys
import uuid


def get_wifi_info():
    try:
        if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            process = subprocess.Popen(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
                stdout=subprocess.PIPE)
            out, err = process.communicate()
            process.wait()
            wifi_info = "".join(map(chr, out))
            print(wifi_info)
            return wifi_info
        elif sys.platform in ['Windows', 'win32', 'cygwin']:
            wifi_info = os.popen("Netsh WLAN show interfaces").readlines()
            print(wifi_info)
            return wifi_info
        else:
            return None
    except Exception as e:
        print(e)
        return None


def get_username():
    try:
        username = getpass.getuser()
        print("Username: " + username)
        return username
    except Exception as e:
        print(e)
        return None


def get_homedir():
    try:
        homedir = os.path.expanduser("~")
        print("Home Directory: " + homedir)
        return homedir
    except Exception as e:
        print(e)
        return None


def get_hostname():
    try:
        hostname = socket.gethostname()
        print("Hostname: " + hostname)
        return hostname
    except Exception as e:
        print(e)
        return None


def get_alt_homedir():
    try:
        alt_homedir = platform.node()
        print("Alt Hostname: " + alt_homedir)
        return alt_homedir
    except Exception as e:
        print(e)
        return None


def get_host_name_by_address():
    try:
        hostname_by_address = socket.gethostbyaddr(socket.gethostname())
        print("Hostname by Address: " + str(hostname_by_address))
        return hostname_by_address
    except Exception as e:
        print(e)
        return None


def get_ip_address():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        print("IP Address: " + ip_address)
        return ip_address
    except Exception as e:
        print(e)
        return None


def get_mac_address():
    try:
        mac_address = hex(uuid.getnode())
        print("MAC Address: " + mac_address)
        return mac_address
    except Exception as e:
        print(e)
        return None


def get_formatted_mac_address():
    try:
        mac_address = hex(uuid.getnode())
        print("MAC Address: " + mac_address)
        print("Formatted MAC address: ", end="")
        print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
        return mac_address
    except Exception as e:
        print(e)
        return None


def get_user_details():
    get_wifi_info()


if __name__ == '__main__':
    get_user_details()
