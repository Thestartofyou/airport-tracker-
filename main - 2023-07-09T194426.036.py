import requests
import json

api_key = "YOUR_API_KEY"
tail_number = "N628TS"

def get_aircraft_location(tail_number):
    url = f"https://adsbexchange.com/api/aircraft/json/icao/{tail_number}/"
    headers = {"api-auth": api_key}

    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.content)
        
        if "ac" in data:
            aircraft = data["ac"]
            latitude = aircraft["lat"]
            longitude = aircraft["lon"]
            altitude = aircraft["alt_baro"]
            
            print(f"Tail Number: {tail_number}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Altitude: {altitude} feet")
        else:
            print("Aircraft not found.")
    
    except requests.exceptions.RequestException as e:
        print("An error occurred while accessing the API:", str(e))

# Example usage:
get_aircraft_location(tail_number)
