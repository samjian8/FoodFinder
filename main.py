from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Preferences(BaseModel):
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

@app.post("/ping")
def ping():
    return {"ping": "ok"}
