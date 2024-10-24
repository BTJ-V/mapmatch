import json
import folium
import os


if not os.path.exists("data.geojson"):
    print("GeoJSON file not found. Make sure 'data.geojson' is saved in the script directory.")
else:

    with open("data.geojson") as f:
        geojson_data = json.load(f)

    coordinates = []
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'LineString':
            coordinates = feature['geometry']['coordinates']

    # Check if coordinates are found
    if coordinates:
        # Calculate the midpoint for better map centering
        latitudes, longitudes = zip(*coordinates)
        map_center = [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]

        # Create a map centered on the midpoint
        m = folium.Map(location=map_center, zoom_start=14)

        # Add a polyline for the route
        folium.PolyLine(locations=coordinates, color='blue').add_to(m)

        # Save the route map
        m.save("route_map.html")
        print("Route calculated and saved as 'route_map.html'.")
    else:
        print("No valid coordinates found in the GeoJSON file.")
