import os
import dotenv
import requests

dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

params = {
    "location": "43.6452,-79.3806",
    "radius": 1000,  # meters
    "type": "restaurant",
    "keyword": "japanese",  # e.g., "sushi", "italian", "mexican"
    "key": GOOGLE_API_KEY,
}
r = requests.get(
    "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
    params=params, timeout=10
)
data = r.json()
print(data)