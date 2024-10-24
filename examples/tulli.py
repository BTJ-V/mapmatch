import requests
import json

# Replace with your TollGuru API key
API_KEY = "Tg6dTd642bfdJnjrpGpqtb92hmBqGng3"

# Define the start, end, and waypoints of your path
coordinates = [
    {"lat": 40.712776, "lng": -74.005974},  # Example: Start point (New York)
    {"lat": 41.878113, "lng": -87.629799}   # Example: End point (Chicago)
]

# Optional: You can add more intermediate waypoints if necessary
waypoints = [
    {"lat": 39.099724, "lng": -94.578331}  # Example: Waypoint (Kansas City)
]

# Prepare the request data
data = {
    "source": coordinates[0],
    "destination": coordinates[1],
    "waypoints": waypoints,
    "vehicleType": "2AxlesAuto",  # Modify based on your vehicle type
    "fuelPrice": 3,  # Example: Fuel price in USD per gallon (optional)
    "fuelEfficiency": 25,  # Fuel efficiency (miles per gallon)
    "currency": "USD"
}

# Set headers with the API key
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Send the request
response = requests.post("https://api.tollguru.com/v1/calc/route", headers=headers, data=json.dumps(data))

# Parse the response
if response.status_code == 200:
    result = response.json()
    toll_cost = result.get("route", {}).get("costs", {}).get("tag", {}).get("currency", "USD") + " " + str(result.get("route", {}).get("costs", {}).get("tag", {}).get("value", 0))
    print(f"Total toll cost: {toll_cost}")
else:
    print(f"Error: {response.status_code} - {response.text}")
