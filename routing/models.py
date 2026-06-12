from django.db import models

# Create your models here.


class FuelStation(models.Model):
    truckstop_id = models.IntegerField()

    name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=10)

    rack_id = models.IntegerField()

    fuel_price = models.DecimalField(max_digits=6, decimal_places=3)

    latitude = models.FloatField(null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"


class LocationMapping(models.Model):
    """table for co-ordinates that are used in inputs"""
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )

    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "location_mappings"

    def __str__(self):
        return self.name