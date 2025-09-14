from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import fetcher, normalize, scoring
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Restaurants(BaseModel):
    place_id: str
    name: Optional[str] = None
    rating: Optional[float] = None
    ratings_count: Optional[int] = None
    price_level: Optional[int] = None   # 0–4
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None
    open_now: Optional[bool] = None
    types: List[str] = []

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

@app.post("/ping")
def ping():
    return {"ping": "ok"}

@app.get("/recommend", response_model=List[Restaurants])
async def recommend(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"), 
    radius: int = Query(1000, ge=1, le=50000, description="Search radius in meters")
):
    try:
        raw_places = fetcher.fetch_nearby_restaurants(lat, lng, radius)
    except ValueError as e:
        # API key or API response issues
        raise HTTPException(status_code=400, detail=f"Configuration or API error: {str(e)}")
    except ConnectionError as e:
        # Network or connection issues
        raise HTTPException(status_code=502, detail=f"Unable to connect to service: {str(e)}")
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    normalized_places = [normalize.normalize_place(p) for p in raw_places]

    # Try to filter for explicitly open restaurants
    open_places = scoring.filter_open_now(normalized_places)
    
    # Apply scoring to get best recommendations
    scored_places = []
    
    # Get best overall restaurant
    best = scoring.best_overall(open_places)
    if best:
        scored_places.append(best)
    
    # Get best cheap option
    cheap = scoring.best_cheap_option(open_places)
    if cheap and cheap not in scored_places:  # Avoid duplicates
        scored_places.append(cheap)
    
    # Get hidden gem
    gem = scoring.pick_hidden_gem(open_places)
    if gem and gem not in scored_places:  # Avoid duplicates
        scored_places.append(gem)
    
    return [Restaurants(**place) for place in scored_places]