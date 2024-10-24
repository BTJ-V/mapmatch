import json
import csv

def convert_geojson_to_csv(geojson_file, csv_file):
    """
    Convert GeoJSON file with LineString to CSV with latitude and longitude.
    
    Parameters:
    - geojson_file: Path to the input GeoJSON file.
    - csv_file: Path to the output CSV file.
    """
    with open(geojson_file) as f:
        geojson_data = json.load(f)

    coordinates = []
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'LineString':
            # Append each coordinate to the list
            coordinates.extend(feature['geometry']['coordinates'])

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["latitude", "longitude"])  # Write header
        for lat, lon in coordinates:
            writer.writerow([lat, lon])  # Write each coordinate pair

    print(f"CSV file '{csv_file}' created successfully with {len(coordinates)} points.")

# Convert the GeoJSON file to CSV
convert_geojson_to_csv('data.geojson', 'kukkatpally_trace.csv')
