import os
import dotenv
import requests

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

lat = '43.6452'
lon = '-79.3806'
radius = 1000 # in meters

url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=1000&type=restaurant&key={GOOGLE_API_KEY}"
response = requests.get(url=url)
print(response.json())
