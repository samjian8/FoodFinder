from typing import List, Dict, Any, Optional, Tuple

def overall_rating_key(place: Dict[str, Any]):
    '''
    Arranges a singular place into a tuple of key elements, in a specified order for sorting.
    '''
    # higher rating first, then more reviews, then name/place_id for determinism
    return (place.get("rating") or 0.0, place.get("ratings_count") or 0, place.get("name") or "", place.get("place_id") or "")

