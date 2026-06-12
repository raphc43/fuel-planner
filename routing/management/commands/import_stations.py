import pandas as pd

from django.core.management.base import BaseCommand

from routing.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel stations from CSV"

    def handle(self, *args, **kwargs):

        df = pd.read_csv("fuel-prices-for-be-assessment.csv")

        FuelStation.objects.all().delete()

        stations = []

        for _, row in df.iterrows():

            stations.append(
                FuelStation(
                    truckstop_id=row["OPIS Truckstop ID"],
                    name=row["Truckstop Name"],
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    rack_id=row["Rack ID"],
                    fuel_price=row["Retail Price"],
                )
            )

        FuelStation.objects.bulk_create(
            stations,
            batch_size=500
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(stations)} stations"
            )
        )