import time
import requests

from django.core.management.base import BaseCommand
from routing.models import FuelStation


class Command(BaseCommand):
    help = "Geocode all fuel stations using Nominatim"

    def handle(self, *args, **kwargs):

        stations = FuelStation.objects.filter(
            latitude__isnull=True,
            longitude__isnull=True,
            state__in=["NJ", "MD", "VA", "NC", "SC", "GA", "FL"]
        )[:20]

        self.stdout.write(f"Geocoding {stations.count()} stations...")

        for i, station in enumerate(stations, start=1):

            query = f"{station.city}, {station.state}, USA"

            try:
                response = requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={
                        "q": query,
                        "format": "json",
                        "limit": 1
                    },
                    headers={
                        "User-Agent": "fuel_planner-app"
                    },
                    timeout=10
                )

                data = response.json()

                if data:
                    station.latitude = float(data[0]["lat"])
                    station.longitude = float(data[0]["lon"])
                    station.save()

                    self.stdout.write(
                        f"[{i}] OK: {station.name} → {station.latitude}, {station.longitude}"
                    )
                else:
                    self.stdout.write(
                        f"[{i}] NOT FOUND: {query}"
                    )

            except Exception as e:
                self.stdout.write(
                    f"[{i}] ERROR: {query} → {str(e)}"
                )

            # IMPORTANT: avoid rate limit
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Geocoding completed"))