import os
import dotenv
import requests

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



def fetch_nearby_restaurants(lat, lng, radius):
    if not GOOGLE_API_KEY:
        raise ValueError("Missing GOOGLE_API_KEY environment variable")
    
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=restaurant&key={GOOGLE_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # This raises HTTPError for bad status codes (4XX, 5XX)
    except requests.RequestException as e:
        raise ConnectionError(f"Network error: {e}")
    
    data = response.json()
    if data.get("status") != "OK":
        raise ValueError(f"Places API status: {data.get('status')}")
    
    return data.get("results", [])