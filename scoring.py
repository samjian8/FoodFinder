from typing import List, Dict, Any, Optional, Tuple

def overall_rating_key(p: Dict[str, Any]):
    '''
    Arranges a singular place into a tuple of key elements, in a specified order for sorting.
    '''
    # higher rating first, then more reviews, then name/place_id for determinism
    return (p.get("rating") or 0.0, p.get("ratings_count") or 0, p.get("name") or "", p.get("place_id") or "")

def best_overall(places: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    '''
    Returns the top place sorted by overall rating.
    If there are no places, returns None.
    '''
    sorted_places = sorted(places, key=overall_rating_key, reverse=True)
    return sorted_places[0] if sorted_places else None

def best_cheap_option(places: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    '''
    Returns the top place sorted by overall rating, but only among those with price_level 0 or 1.
    If there are no such places, returns None.
    '''
    cheap_places = [p for p in places if (p.get("price_level") is not None and p.get("price_level") <= 1)]
    sorted_cheap_places = sorted(cheap_places, key=overall_rating_key, reverse=True)
    return sorted_cheap_places[0] if sorted_cheap_places else None

def pick_hidden_gem(places: List[Dict[str, Any]], max_reviews: int = 70) -> Optional[Dict[str, Any]]:
    '''
    Picks a "hidden gem" restaurant that has a high rating but relatively few reviews.
    '''
    cand = [p for p in places if (p.get("ratings_count") or 0) < max_reviews and (p.get("rating") or 0) >= 4.0]
    if not cand:
        return None
    top = sorted(cand, key=overall_rating_key, reverse=True)[0]
    return top

