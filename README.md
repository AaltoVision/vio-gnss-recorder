# VIO-GNSS Recorder
Automatisation of [SpectacularAI's GNSS + VIO demo](https://github.com/SpectacularAI/docs/blob/main/pdf/GNSS-VIO_OAK-D_Python.pdf). Including some added functionalities to make collecting data easier.
The purpose of this software is to alleviate collecting and analyzing large datasets with SpectacularAI's GNSS-VIO Fusion implementation.

### Automatisation
* The script `vio_gnss_recorder.py` asks the user to input some basic information like the authentication credentials for a RTK provider + the user's approximate location.
* The script initializes [NTRIP](https://en.wikipedia.org/wiki/Networked_Transport_of_RTCM_via_Internet_Protocol) and the sensor fusion pipeline in the background.
* After user input the script starts to print the relative pose of the OAK-D device:
<img src="/assets/images/before_alignment.png" width="900" alt="Before trajectory alignment" title="GNSS and  VIO trajectories have not aligned"/>

* User should wait for the module to acquire a RTK Fix (which can be observed from the board's yellow LED). Then traversing 20 to 50 meters should make the trajectories align. The output looks something like this after achieving the sensor fusion phase:
<img src="/assets/images/after_alignment.png" width="900" alt="After trajectory alignment" title="Sensor Fusion has been achieved"/>
 

### Map
* A map showing the travelled route is rendered. The route is determined after Sensor Fusion in the pipe which means that the route should attain a satisfactory accuracy even when temporarily travelling in a GPS dead zone.
* The map indicates the state of the RTK solution (None, Float, Fix) with colored markers
* **TODO:** At the moment, the script utilizes the real-time location output of the system to render the map. This means that **SLAM** won't correct the rendered route 'in the past'. A functionality could be added so that the map renderer can take SLAM's corrections into account.

Example map (OpenStreetMap):                                 
<img src="/assets/images/map_test.png" width="400" alt="Example Map" title="Otaniemi, Espoo, Finland"/>
