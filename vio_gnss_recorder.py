"""
See https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf
for an example of what this script aims to automate.

The script needs the absolute paths to clones of AaltoVision/u-blox-capture and AaltoVision/sdk-examples which are defined in the file 'config.ini'.

The script draws a map which shows the RTK solution's state during the traversal by colored dots.

Running the script requires an internet connnection for RTK's correction data and fetching the map template from the web.

"""

import getpass
import readline

import configparser

# 'Define' the absolute paths of the directories this script depends on
configuration = configparser.ConfigParser()
configuration.read("config.ini")
U_BLOX_CAPTURE_PATH = configuration['Filepaths']['u-blox-capture']
SDK_EXAMPLES_PATH = configuration['Filepaths']['sdk-examples']

# Is the user logged in as sudo?
print("\nYou are logged in as " + getpass.getuser() + "\n")

### Ask credentials, mountpoint address, rough coordinates...
print("Your RTK providers credentials:")
user = input("Username: ")
password = getpass.getpass()
print("\n")
address = input("RTK provider's IP address eg. 'xyz.abc.com': ")
port = input("Port: ")
mountpoint = input("Specify the used mountpoint: ")

# Validate correct format for coordinates, accept '.' and '-'
while True:
    wrongFormat = "Wrong format. Try again using the correct format, like this: 60.2 24.8"
    try:
        lat, lon = input("Type the coordinates of your current location in format 'LAT LON' (use . as a decimal separator):\n").split()
        if not float(lat) and not float(lon):
            print(wrongFormat)
            continue
    except ValueError:
        print(wrongFormat)
        continue
    else:
        break

