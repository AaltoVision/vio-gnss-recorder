# VIO-GNSS Recorder
Automatisation of [SpectacularAI's GNSS + VIO demo](https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf). Including some added functionalities to make collecting data easier.
The purpose of this software is to alleviate collecting and analyzing large datasets with SpectacularAI's GNSS-VIO Fusion implementation.
> #### Necessary hardware[^pdf]:
> - u-blox C099-F9P board + ANN-MB-00 antenna
> - Luxonis OAK-D camera
> - Laptop running Linux

## Automatisation
* The script `vio_gnss_recorder.py` asks the user to input some basic information like the authentication credentials for a RTK provider + the user's approximate location.
* The script initializes [NTRIP](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) and the sensor fusion pipeline in the background.
* After user input the script starts to print the relative pose of the OAK-D device:
<img src="/assets/images/before_alignment.png" width="900" alt="Before trajectory alignment" title="GNSS and  VIO trajectories have not aligned"/>

* User should wait for the module to acquire a RTK Fix (which can be observed from the board's yellow LED). Then traversing 20 to 50 meters should make the trajectories align. The output looks something like this after achieving the sensor fusion phase:
<img src="/assets/images/after_alignment.png" width="900" alt="After trajectory alignment" title="Sensor Fusion has been achieved"/>

* The dataset is saved in a `session<timestamp>` folder. 
 
## Map
* A map showing the travelled route is rendered. The route is determined after Sensor Fusion in the pipe which means that the route should attain a satisfactory accuracy even when temporarily travelling in a GPS dead zone.
* The map indicates the state of the RTK solution (None, Float, Fix) with colored markers. *RTK Fix solution usually corresponds to an accuracy of only few centimeters.*[^rtk]
* **TODO:** At the moment, the script utilizes the real-time location output of the system to render the map. This means that **SLAM** won't correct the rendered route 'in the past'. A functionality could be added so that the map renderer can take SLAM's corrections into account.

Example map (OpenStreetMap):                                 
<img src="/assets/images/map_test.png" width="400" alt="Example Map" title="Otaniemi, Espoo, Finland"/>

## Setup
> *It is recommended to test the aforementioned demonstration because this implementation utilizes its components under the hood.*

This software should be setup and ran inside a Python virtual environment to avoid any conflicts.
<details open>
<summary>Virtual environments with Python.</summary>
 
```bash
pip install virtualenv
# Create and navigate into your project folder
python -m venv <env_name>
# To activate
. <env_name>/bin/activate
# To deactivate
deactivate
```

</details>

Start by cloning this repository.
```bash
git clone https://github.com/AaltoVision/vio_gnss_recorder
```
### Configure u-blox C099-F9P board
You'll need to configure the board (instructions in the [PDF](https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf)) for which you can use AaltoVision's fork of the `u-blox-capture` repository[^u-blox-repo] because you'll need it later on to communicate with the board.
```bash
git clone https://github.com/AaltoVision/u-blox-capture --recurse-submodules
```

If the board configuration is not flashed permamently, the configuration has to be done prior to running `vio_gnss_recorder.py` so after every reconnection or reboot.
**Important:** `vio_gnss_recorder.py` **does not configure the board automatically.**

After cloning `u-blox-capture` you'll need to build `str2str`
```bash
cd RTKLIB/app/str2str/gcc/
make
```
### Dependencies
After activating your virtual environment, install all the packages with `pip`
```bash
pip install -r requirements.txt
```
### RTK/NTRIP configuration
**TODO**

[^pdf]: https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf — © Spectacular AI
[^rtk]: https://sciencing.com/difference-between-rtk-fix-rtk-float-12245568.html
[^u-blox-repo]: https://github.com/AaltoML/u-blox-capture
