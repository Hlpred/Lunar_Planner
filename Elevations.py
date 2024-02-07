#Unused test code

import requests

# Set the latitude and longitude of the location you want to retrieve elevation for
lat = 0.0
lon = 23.0

# Set the URL for the Moon Trek API and the API key
url = "https://trek.nasa.gov/tiles/Moon/EQ/LRO_LrocKaguya_Shade_60N60S_512ppd"
api_key = "EvJOsg5OiANoiaX1dd2fCOnFqcDKYycuBHHcLhD3"

# Set the query parameters for the API request
params = {
    "lat": lat,
    "lon": lon,
    "alt": 0,
    "output": "json",
    "api_key": api_key,
}

# Send the API request
response = requests.get(url, params=params)

# Parse the JSON response to retrieve the elevation value
elevation = response.json()["elevation"]

# Print the elevation value
print(f"The elevation at ({lat}, {lon}) is {elevation} meters.")
