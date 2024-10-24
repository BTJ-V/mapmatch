import requests
import json
import csv

def fetch_overpass_data(node_ids):
    # Construct Overpass API query
    query = f"""
        [out:json];
        (
            {' '.join([f'node({node_id});' for node_id in node_ids])}
        );
        out;
    """
    
    # Send POST request to Overpass API
    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data={"data": query},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    # Return JSON response
    return response.json()

def get_osrm_route(source, destination):
    # Construct OSRM API URL using the provided source and destination coordinates
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{source};{destination}?overview=full&annotations=true"
    
    # Send GET request to OSRM API
    response = requests.get(osrm_url)
    
    # Return OSRM response in JSON format
    return response.json()

def process_osrm_response(osrm_response):
    # Extract node IDs from the OSRM response for all legs
    node_ids = []
    for route in osrm_response['routes']:
        for leg in route['legs']:
            node_ids.extend(leg['annotation']['nodes'])
    
    # Fetch Overpass API data using the extracted node IDs
    overpass_data = fetch_overpass_data(node_ids)
    
    # Extract coordinates from Overpass API response
    coordinates = []
    for element in overpass_data['elements']:
        if element['type'] == 'node':
            lat = element['lat']
            lon = element['lon']
            coordinates.append((lat, lon))
    
    # Save coordinates to CSV file
    with open('source_to_destination_trace.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['latitude', 'longitude'])
        writer.writerows(coordinates)

# Specify source and destination as "longitude,latitude" strings
source = "78.3953, 17.4875" # Example: Bangalore City Center (Source)
destination = "78.5285, 17.2173"  # Example: West of Bangalore (Destination)

# Get OSRM route between source and destination
osrm_response = get_osrm_route(source, destination)

# Process the OSRM response to extract and save coordinates
process_osrm_response(osrm_response)
