def normalize_place(p: dict) -> dict:
    loc = (p.get("geometry") or {}).get("location") or {}
    return {
        "place_id": p.get("place_id"),
        "name": p.get("name"),
        "rating": p.get("rating"),
        "ratings_count": p.get("user_ratings_total"),
        "price_level": p.get("price_level"),
        "lat": loc.get("lat"),
        "lng": loc.get("lng"),
        "address": p.get("vicinity") or p.get("formatted_address"),
        "open_now": (p.get("opening_hours") or {}).get("open_now"),
        "types": p.get("types") or [],
    }
