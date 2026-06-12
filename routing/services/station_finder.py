from routing.models import FuelStation
from routing.services.geo_utils import haversine


def get_stations_near_route(route_points, max_distance=20):

    candidates = []

    stations = FuelStation.objects.exclude(latitude=None)

    for station in stations:

        for lon, lat in route_points[::50]:
            distance = haversine(
                lat,
                lon,
                station.latitude,
                station.longitude
            )

            if distance <= max_distance:

                candidates.append(station)
                break

    return candidates