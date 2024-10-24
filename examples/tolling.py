import csv
from pathlib import Path
from pyproj import Transformer
from mappymatch.constructs.trace import Trace
from mappymatch.maps.nx.nx_map import NxMap
from mappymatch.matchers.lcss.lcss import LCSSMatcher
from mappymatch.matchers.line_snap import LineSnapMatcher

PLOT = True

if PLOT:
    import webbrowser
    from mappymatch.utils.plot import plot_matches

# Load trace from CSV file
trace = Trace.from_csv("./directions.csv")

# Generate a geofence polygon around the trace
geofence = Geofence.from_trace(trace, padding=1e3)

# Pull a networkx map from the OSM database
nx_map = NxMap.from_geofence(geofence)

# Initialize matchers
lcss_matcher = LCSSMatcher(nx_map)
snap_matcher = LineSnapMatcher(nx_map)

# Perform matching
lcss_matches = lcss_matcher.match_trace(trace)
snap_matches = snap_matcher.match_trace(trace)

# Transformer to convert EPSG:3857 (Web Mercator) to EPSG:4326 (lat/lon)
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")

# Prepare a list to store converted coordinates
converted_coordinates = []

# Extract and convert coordinates from lcss_matches
for match in lcss_matches.matches:
    line = match.road.geom  # Assuming this is the linestring geometry
    for x, y in line.coords:  # Extract the coordinates
        lon, lat = transformer.transform(x, y)  # Convert to lat/lon
        converted_coordinates.append([lat, lon])

# Save converted coordinates to CSV
csv_file = 'lcss_converted_coordinates.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Latitude', 'Longitude'])  # CSV header
    writer.writerows(converted_coordinates)

print(f"Coordinates saved to {csv_file}")

# Plot and open matches if PLOT is True
if PLOT:
    lcss_file = Path("lcss_matches.html")
    lmap = plot_matches(lcss_matches.matches)
    lmap.save(str(lcss_file))
    webbrowser.open(lcss_file.absolute().as_uri())

    smap_file = Path("snap_matches.html")
    smap = plot_matches(snap_matches.matches)
    smap.save(str(smap_file))
    webbrowser.open(smap_file.absolute().as_uri())
