def build_fuel_plan(distance, stations):
    # Truck/car fuel efficiency: 10 miles per gallon
    MPG = 10

    # Maximum distance that can be traveled on a full tank
    RANGE = 500

    # Stores each refueling segment of the trip
    plan = []

    # Miles left to travel
    remaining = distance

    # Current position in the trip
    current_mile = 0

    # Continue until the entire trip distance is covered
    while remaining > 0:

        # Travel either the full tank range or the remaining distance
        travel = min(RANGE, remaining)

        # Select the station with the lowest fuel price
        # (simple strategy: always buy fuel at the cheapest station)
        best_station = min(stations, key=lambda x: x.fuel_price)

        # Calculate gallons needed for this segment
        fuel_needed = travel / MPG

        # Calculate fuel cost for this segment
        cost = fuel_needed * float(best_station.fuel_price)

        # Save segment details
        plan.append({
            "from": current_mile,
            "to": current_mile + travel,
            "station": best_station.name,
            "price": float(best_station.fuel_price),
            "cost": round(cost, 2),
        })

        # Move forward along the route
        current_mile += travel
        remaining -= travel

    # Calculate total trip fuel cost
    total_cost = sum(p["cost"] for p in plan)

    # Return detailed fueling plan and total cost
    return plan, total_cost