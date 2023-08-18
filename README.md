# VIO-GNSS Recorder
Automatisation of [SpectacularAI's GNSS + VIO demo](https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf). Including some added functionalities to make collecting data easier.
The purpose of this software is to alleviate collecting and analyzing large datasets with SpectacularAI's GNSS-VIO Fusion implementation.  

If you have access to a 3D printer, you can use the models provided in [`/3D_print`](/3D_print) to print a casing which makes it easier to collect datasets.

> #### Necessary hardware[^pdf]:
> - u-blox C099-F9P board + ANN-MB-00 antenna
> - Luxonis OAK-D camera
> - Laptop running Linux
>
> Take to account that the antenna likely needs a [ground plane](https://www.electronics-notes.com/articles/antennas-propagation/grounding-earthing/antenna-ground-plane-theory-design.php) to work properly. In our setup a thin circular plane of aluminium worked perfectly fine. The antenna can also be mounted on a car for this purpose.

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
* **TODO:** At the moment, the script utilizes the real-time location output of the system to render the map. This means that [SLAM](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) won't correct the rendered route 'in the past'. A functionality could be added so that the map renderer can take SLAM's corrections into account.
                      
<p align="center"><img src="/assets/images/map_test.png" width="400" alt="Example Map" title="Otaniemi, Espoo, Finland"/>
<br><em>Example map output (tile provided by OpenStreetMap)</em></p>

## Setup
> *It is recommended to test the aforementioned demonstration because this implementation utilizes its components under the hood.*

This software should be setup and ran inside a Python virtual environment to avoid any conflicts.
<details>
<summary>Virtual environments in Python.</summary>
 
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
You'll need to configure the board (instructions also in the [PDF](https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf)). Clone AaltoVision's fork of the `u-blox-capture` repository[^u-blox-repo].
```bash
git clone https://github.com/AaltoVision/u-blox-capture --recurse-submodules
```
Navigate to your local copy of the repository.
```bash
# for temporary configuration
python ubx_configurator.py DEVICE_PATH example/high_precision_gps_only.cfg
# for permament configuration
python ubx_configurator.py DEVICE_PATH -flash example/high_precision_gps_only.cfg
```

If the board configuration is not flashed permamently, the configuration has to be done prior to running `vio_gnss_recorder.py` so after every reconnection or reboot.
**Important: `vio_gnss_recorder.py` does not configure the board automatically.**

After cloning `u-blox-capture` you'll need to build `str2str`
```bash
cd RTKLIB/app/str2str/gcc/
make
```
### Dependencies
After activating your virtual environment, install all the necessary packages with `pip`
```bash
pip install -r requirements.txt
```
### Modify `config.ini`
There's a configuration file `config.ini` in the parent directory. The absolute paths to the cloned repositories must be provided there so that `vio_gnss_recorder.py` can use them.
Also the device path must be disclosed. The path is usually `/dev/ttyACM0` but the user can define the path in the case that they have other peripherals in their setup. It should be considered that the number (<code>/dev/ttyACM<b>0</b></code>) increments between reconnections of the module so if the board needs to be disconnected momentarily the user must either modify the config file or reboot the OS.

## Usage
The workflow for using this automatisation:
1. **Record the data**: `python vio_gnss_recorder.py`
   - You might need sudo rights to communicate with OAK-D in your setup. Either modify udev rules accordingly or use  
     `sudo env "PATH=$PATH" python vio_gnss_recorder.py`
   - The board has an yellow LED which indicates the RTK solution's state:
       - Off: None
       - Blinking: Float
       - On: Fix
   - After acquiring a stable RTK Fix, you should move to align the trajectories. The dataset should be collected after the script starts outputting the global position.
   - `Ctrl+C` to stop the program. The dataset is saved in a `session<timestamp>` folder. Locational data points for rendering the map are saved in `coords.txt`.
2. **Render the map**: `python render_map.py`
   - Renders a map of the traversed route using data points parsed from `coords.txt`.
   - Asks the user to type some kind of an identifier (eg. `Otaniemi_14_8_2023`) for the .png to be created.

[^pdf]: https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf — © Spectacular AI
[^rtk]: https://sciencing.com/difference-between-rtk-fix-rtk-float-12245568.html
[^u-blox-repo]: https://github.com/AaltoML/u-blox-capture and https://github.com/SpectacularAI/u-blox-capture
