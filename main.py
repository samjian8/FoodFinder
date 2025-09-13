from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Preferences(BaseModel):
    lat: float
    lng: float
    radius_m: int = 1500
    budget_min: Optional[int] = 1
    budget_max: Optional[int] = 4
    cuisine_kw: Optional[List[str]] = []
    max_km: Optional[float] = 2.0

@app.post("/ping")
def ping():
    return {"ping": "ok"}
