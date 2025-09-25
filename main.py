from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import fetcher, normalize, scoring
from pydantic import BaseModel
from typing import List, Optional
import time
import logging

# Set up logging to see timing info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    start_time = time.time()
    logger.info(f"Starting recommendation pipeline for radius: {radius}m")
    
    try:
        # Step 1: Fetch raw places from API
        fetch_start = time.time()
        raw_places = fetcher.fetch_nearby_restaurants(lat, lng, radius)
        fetch_time = time.time() - fetch_start
        logger.info(f"Fetching took: {fetch_time:.3f}s")
        
    except ValueError as e:
        logger.error(f"API error after {time.time() - start_time:.3f}s: {e}")
        raise HTTPException(status_code=400, detail=f"Configuration or API error: {str(e)}")
    except ConnectionError as e:
        logger.error(f"Connection error after {time.time() - start_time:.3f}s: {e}")
        raise HTTPException(status_code=502, detail=f"Unable to connect to service: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error after {time.time() - start_time:.3f}s: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    # Step 2: Normalize places
    normalize_start = time.time()
    normalized_places = [normalize.normalize_place(p) for p in raw_places]
    normalize_time = time.time() - normalize_start
    logger.info(f"Normalization took: {normalize_time:.3f}s")

    # Step 3: Filter for open restaurants
    filter_start = time.time()
    open_places = scoring.filter_open_now(normalized_places)
    filter_time = time.time() - filter_start
    logger.info(f"Filtering took: {filter_time:.3f}s")
    
    # Step 4: Apply scoring algorithms
    scoring_start = time.time()
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
    
    scoring_time = time.time() - scoring_start
    total_time = time.time() - start_time
    
    logger.info(f"Scoring took: {scoring_time:.3f}s")
    logger.info(f"TOTAL PIPELINE TIME: {total_time:.3f}s")
    
    return [Restaurants(**place) for place in scored_places]