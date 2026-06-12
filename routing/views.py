from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.geocoding_service import run_concurrent_geocoding
from .services.route_service import get_route
from .services.station_finder import get_stations_near_route
from .services.fuel_optimizer import build_fuel_plan

# Serializers
from .serializers import RouteRequestSerializer


class RouteAPIView(APIView):

    def post(self, request):

        try:
            serializer = RouteRequestSerializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)

            start = serializer.validated_data["start"]
            end = serializer.validated_data["end"]

            if not start or not end:
                return Response(
                    {"error": "start and end are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convert addresses into coordinates (fetch from DB, if not found then call API + store it)
            start_coords, end_coords = run_concurrent_geocoding(start, end)

            # Get route from OSRM (single API call)
            route_data = get_route(start_coords, end_coords)

            distance_miles = route_data["distance_miles"]
            geometry = route_data["geometry"]

            # Get stations near route (from Database)
            stations = get_stations_near_route(geometry)

            if not stations:
                return Response(
                    {"error": "No stations found near route"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Build fuel plan (500 mile segments)
            fuel_plan, total_cost = build_fuel_plan(
                distance_miles,
                stations
            )

            # Final response
            return Response({
                "distance_miles": round(distance_miles, 2),
                "fuel_plan": fuel_plan,
                "total_fuel_cost": round(total_cost, 2),
                "route_points": len(geometry)
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )