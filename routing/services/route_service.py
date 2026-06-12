import requests
from django.core.cache import cache


def get_route(start_coords, end_coords):
    base_url = "http://router.project-osrm.org/route/v1/driving/"

    coords = f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"

    url = f"{base_url}{coords}?overview=full&geometries=geojson"

    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("code") != "Ok":
        raise Exception(f"OSRM failed: {data}")

    route = data["routes"][0]

    distance_miles = route["distance"] * 0.000621371
    geometry = route["geometry"]["coordinates"]

    result = {
        "distance_miles": distance_miles,
        "geometry": geometry
    }

    return result