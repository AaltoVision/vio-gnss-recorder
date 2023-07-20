"""
See https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf
for an example of what this script aims to automate.

The script needs the absolute paths to clones of AaltoVision/u-blox-capture and AaltoVision/sdk-examples which are defined in the file 'config.ini'.

The script draws a map which shows the RTK solution's state during the traversal by colored dots.

Running the script requires an internet connnection for RTK's correction data and fetching the map template from the web.

"""

import configparser

# 'Define' the absolute paths of the directories this script depends on
configuration = configparser.ConfigParser()
configuration.read("config.ini")
U_BLOX_CAPTURE_PATH = configuration['Filepaths']['u-blox-capture']
SDK_EXAMPLES_PATH = configuration['Filepaths']['sdk-examples']


