import requests


def get_route(start_coords, end_coords):
    # OSRM public routing API endpoint
    base_url = "http://router.project-osrm.org/route/v1/driving/"

    # Build coordinate string:
    coords = f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"

    # Request full route geometry in GeoJSON format
    url = f"{base_url}{coords}?overview=full&geometries=geojson"

    # Call OSRM API
    response = requests.get(url, timeout=10)
    data = response.json()

    # Verify routing was successful
    if data.get("code") != "Ok":
        raise Exception(f"OSRM failed: {data}")

    # Get first (best) route returned
    route = data["routes"][0]

    # Convert route distance from meters to miles
    distance_miles = route["distance"] * 0.000621371

    # Extract route path coordinates
    geometry = route["geometry"]["coordinates"]

    # Return route information
    result = {
        "distance_miles": distance_miles,
        "geometry": geometry
    }

    return result