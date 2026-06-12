# routing/services/geocoding_service.py

import requests
from concurrent.futures import ThreadPoolExecutor

from routing.models import LocationMapping  # 👈 adjust if your app name differs

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


# -----------------------------
# External API call
# -----------------------------
def _geocode(location: str):
    response = requests.get(
        NOMINATIM_URL,
        params={
            "q": location,
            "format": "json",
            "limit": 1
        },
        headers={
            "User-Agent": "fuel_planner-app"
        },
        timeout=10
    )

    data = response.json()

    if not data:
        raise Exception(f"Could not geocode: {location}")

    lon = float(data[0]["lon"])
    lat = float(data[0]["lat"])

    return [lon, lat]


# -----------------------------
# DB-first resolver
# -----------------------------
def get_or_geocode(location: str):
    """
    1. Check DB
    2. If found → return cached result
    3. If not → call API, store, return
    """

    obj = LocationMapping.objects.filter(name=location).first()

    if obj:
        return [obj.longitude, obj.latitude]

    coords = _geocode(location)

    LocationMapping.objects.create(
        name=location,
        latitude=coords[1],
        longitude=coords[0],
    )

    return coords


# -----------------------------
# Concurrent resolver (start + end)
# -----------------------------
def run_concurrent_geocoding(start_location: str, end_location: str):
    """
    Runs geocoding in parallel.
    DB is checked first for each location.
    If not found then API call is made (concurrently)
    """

    def resolve(location):
        return get_or_geocode(location)

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_start = executor.submit(resolve, start_location)
        future_end = executor.submit(resolve, end_location)

        start_coords = future_start.result()
        end_coords = future_end.result()

    return start_coords, end_coords