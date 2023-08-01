import staticmaps
import re
import readline
from PIL import Image

coords = []                   # Initialize coordinate list. List's element's are tuples (which are static --> enhance runtime performance)
'''
coords = [
    (lat, lon, rtk),
    (lat, lon, rtk),
    (lat, lon, rtk),
    ...
    ...
]
'''

### Ask for the location where data was collected
while True:
    file_id = input("Type an identifier for the filename (use underscore for whitespace): ")
    if file_id == "" or " " in file_id:
        print("Input either empty or contains whitespace. Try again.")
        continue
    else: break

### Parse the .txt file

filter = r'Global position: ([\d.]+), ([\d.]+); RTK solution: (\w+)'

with open("coords.txt") as file:
    entries = file.readlines()
    for i in entries:
        if re.match(filter, i) == None:   # Hop over the lines where VIO and GNSS haven't synced and anything that regex doesn't find a match in
            continue
        valid_entry = re.match(filter, i)
        lat = float(valid_entry.group(1))
        lon = float(valid_entry.group(2))
        rtk = valid_entry.group(3)
        entry = (lat, lon, rtk)
        coords.append(entry)

### Initialize and render the map using OpenStreetMap
### https://github.com/flopp/py-staticmaps/tree/master like in this example

context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_OSM)

# vio_gnss.py outputs data points so frequently that we can pick every 100th for map markers
for point in coords[::100]:

    location = staticmaps.create_latlng(point[0], point[1])   # Create LatLng object (coordinate point)

    # Set color for marker according to RTK state
    match point[2]:
        case 'None':
            marker_color = "marker_graphics/red_marker.png"
        case 'Float':
            marker_color = "marker_graphics/yellow_marker.png"
        case 'Fix':
            marker_color = "marker_graphics/green_marker.png"
    
    # Add marker to map
    context.add_object(staticmaps.ImageMarker(location, marker_color, 8, 8))

# Find out and set bounds for map
min_lat = min(coords, key= lambda x:x[0])[0]
max_lat = max(coords, key= lambda x:x[0])[0]
min_lon = min(coords, key= lambda x:x[1])[1]
max_lon = max(coords, key= lambda x:x[1])[1]

W = 0.0027  # You cannot pass too small bounds to add_bounds. These are the min. width and height of the tile bounds
H = 0.0027

w = max_lon - min_lon   # Current measures of the box
h = max_lat - min_lat

# If current bounds are too small, increase them to fulfill the requirements. The constant 0.00..01 is there so that float-point arithmetics/rounding
#                                                                             don't bump the values smaller than the requirement.

if w < W:
    diff = W-w
    min_lon -= (diff/2 + 0.0001)
    max_lon += (diff/2 + 0.0001)

if h < H:
    diff = H-h
    min_lat -= (diff/2 + 0.0001)
    max_lat += (diff/2 + 0.0001)

context.add_bounds(staticmaps.parse_latlngs2rect(f"{min_lat},{min_lon} {max_lat},{max_lon}"))

# Render the map

with Image.open("map_legend.png") as legend:

    img = context.render_pillow(1080, 1080)
    filename = f"map_{file_id}.png"
    final = Image.alpha_composite(img, legend)
    final.save(filename)