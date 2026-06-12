def build_fuel_plan(distance_miles, stations):

    range_miles = 500
    fuel_plan = []
    current = 0

    sorted_stations = sorted(stations, key=lambda s: s.fuel_price)
    i = 0

    while current < distance_miles:

        segment_end = min(current + range_miles, distance_miles)

        cheapest = sorted_stations[i % len(sorted_stations)]
        i += 1

        gallons = (segment_end - current) / 10
        cost = gallons * float(cheapest.fuel_price)

        fuel_plan.append({
            "from": round(current, 2),
            "to": round(segment_end, 2),
            "station": cheapest.name,
            "price": float(cheapest.fuel_price),
            "cost": round(cost, 2)
        })

        current = segment_end

    total_cost = sum(x["cost"] for x in fuel_plan)

    return fuel_plan, total_cost