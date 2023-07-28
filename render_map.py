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

### Render the map using OpenStreetMap
### https://github.com/flopp/py-staticmaps/tree/master like in this example

context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_OSM)

for point in coords:

    location = staticmaps.create_latlng(point[0], point[1])   # Create LatLng object (coordinate point)

    # Set color for marker according to RTK state
    match point[2]:
        case 'None':
            marker_color = staticmaps.RED
        case 'Float':
            marker_color = staticmaps.YELLOW
        case 'Fix':
            marker_color = staticmaps.GREEN
    
    # Add marker to map
    context.add_object(staticmaps.Marker(location, color=marker_color, size=5))

# Render the map

with Image.open("map_legend.png") as legend:

    img = context.render_pillow(1080, 1080)
    filename = f"map_{file_id}.png"
    final = Image.alpha_composite(img, legend)
    final.save(filename)