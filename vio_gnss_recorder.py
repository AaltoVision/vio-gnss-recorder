"""
See https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf
for an example of what this script aims to automate.

The script needs the absolute paths to clones of AaltoVision/u-blox-capture and AaltoVision/sdk-examples which are defined in the file 'config.ini'.

The script draws a map which shows the RTK solution's state during the traversal by colored dots.

Running the script requires an internet connnection for RTK's correction data and fetching the map template from the web.

"""

import getpass
import readline
import shlex
import subprocess
from datetime import datetime
import sys

import configparser

# 'Define' colors and styles to make output easier to read
YELLOW = '\033[93m'
BOLD = '\033[1m'
END = '\033[0m'

# Is the user logged in as sudo?
print("\nYou are logged in as " + BOLD + getpass.getuser() + END)
# The module should be configured prior to running this script
print(YELLOW + "The module (u-blox C099-F9P) should be configured prior to running this script.\n" + END)

# 'Define' the absolute paths of the directories this script depends on, also show a warning if paths aren't configured. Device is also defined.
configuration = configparser.ConfigParser()
configuration.read("config.ini")
U_BLOX_CAPTURE_PATH = configuration['Filepaths']['u-blox-capture']
SDK_EXAMPLES_PATH = configuration['Filepaths']['sdk-examples']
DEVICE_PATH = configuration["Filepaths"]['device-path']
DEVICE = DEVICE_PATH.split('/')[-1]
    
if U_BLOX_CAPTURE_PATH == "" or SDK_EXAMPLES_PATH == "" or DEVICE_PATH == "":
    print(YELLOW + "WARNING: Necessary filepaths aren't configured in config.ini\n" + END)

### Ask credentials, mountpoint address, rough coordinates...
print("Your RTK provider's credentials:")
user = input("Username: ")
password = getpass.getpass()
print("\n")
address = input("RTK provider's IP address eg. 'xyz.abc.com': ")
port = input("Port: ")
mountpoint = input("Specify the used mountpoint: ")

# Validate correct format for coordinates, accept '.' and '-'
while True:
    wrongFormat = YELLOW+"Wrong format. Try again using the correct format, like this: 60.2 24.8"+END
    try:
        lat, lon = input("Type the coordinates of your current location in format 'LAT LON' (use . as a decimal separator):\n").split()
        if not float(lat) or not float(lon):
            print(wrongFormat)
            continue
    except ValueError:
        print(wrongFormat)
        continue
    else:
        break
print("\n")

### Check if coords.txt already exists and confirm possible overwrite
try:
    with open('coords.txt', 'x') as f:
        pass
except FileExistsError:
    while True:
        ans = input(YELLOW + "File coords.txt already exists. " + END + "Do you want to overwrite it? [y/n]\n")
        if ans.lower() == 'y': break
        elif ans.lower() == 'n': print("Exiting program..."); exit(0)
        else: print("Invalid syntax, try again")

### Run str2str in the background to pipe RTK signal to the module
STR2STR = shlex.split \
(f"{U_BLOX_CAPTURE_PATH}/RTKLIB/app/str2str/gcc/str2str -in ntrip://{user}:{password}@{address}:{port}/{mountpoint} \
  -p {lat} {lon} 0.0 -n 250 -out serial://{DEVICE}:460800:8:n:1 &")

subprocess.Popen(STR2STR, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # We don't need the output


### Run SpectacularAI's script vio_gnss.py piping the module's coordinates into it. Session is recorded to current folder

# To build the pipe, the commands are separated and the pipe is achieved via subprocess module

VIO_GNSS1 = shlex.split \
(f"python {U_BLOX_CAPTURE_PATH}/ubx_stdout.py {DEVICE_PATH} --json --fixStatus")
# VIO_GNSS1 = shlex.split("python ./sample_ubx_stdout.py")  # portrays ubx_stdout.py for debugging

timestamp = datetime.now().strftime('%d-%m-%y_%H:%M') # timestamp for recording folder
VIO_GNSS2 = shlex.split \
(f"python {SDK_EXAMPLES_PATH}/python/oak/vio_gnss.py ./session_{timestamp}/")

# ubx_stdout.py --> vio_gnss.py --> coords.txt
with open('coords.txt', 'w') as f:
    ubx_stdout = subprocess.Popen(VIO_GNSS1, stdout=subprocess.PIPE, text=True)
    with subprocess.Popen(VIO_GNSS2, stdin=ubx_stdout.stdout, stdout=subprocess.PIPE, universal_newlines=True) as p:
        for line in p.stdout:
            #line.decode('utf-8')
            sys.stdout.write(line)
            f.write(line)
