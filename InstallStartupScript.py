import getpass
import shutil
import os

username = getpass.getuser()
currentDirectory = os.getcwd()
shutil.copy2(currentDirectory+'/RunCheckScripts - Shortcut.lnk', 'C:/Users/'+username+'/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')