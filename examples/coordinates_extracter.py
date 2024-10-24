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

def process_osrm_response(file_path, num_nodes):
    # Read OSRM response from JSON file
    with open(file_path, 'r') as file:
        osrm_response = json.load(file)
    
    # Extract node IDs from OSRM response
    node_ids = osrm_response['routes'][0]['legs'][0]['annotation']['nodes']
    
    # Limit the number of node IDs to fetch
    node_ids = node_ids[:num_nodes]
    
    # Fetch Overpass API data using extracted node IDs
    overpass_data = fetch_overpass_data(node_ids)
    
    # Extract coordinates from Overpass API response
    coordinates = []
    for element in overpass_data['elements']:
        if element['type'] == 'node':
            lat = element['lat']
            lon = element['lon']
            coordinates.append((lat, lon))
    
    # Save coordinates to CSV file
    with open('kukkatpally_trace.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['latitude', 'longitude'])
        writer.writerows(coordinates)

# Example usage: Extract and save coordinates for the first 10 nodes
process_osrm_response('osrm-response.json', 1100)
