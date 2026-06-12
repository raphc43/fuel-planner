def build_fuel_plan(distance, stations):
    MPG = 10
    RANGE = 500

    plan = []
    remaining = distance
    current_mile = 0

    while remaining > 0:
        travel = min(RANGE, remaining)

        # cheapest station (simple + effective)
        best_station = min(stations, key=lambda x: x.fuel_price)

        fuel_needed = travel / MPG
        cost = fuel_needed * float(best_station.fuel_price)

        plan.append({
            "from": current_mile,
            "to": current_mile + travel,
            "station": best_station.name,
            "price": float(best_station.fuel_price),
            "cost": round(cost, 2),
        })

        current_mile += travel
        remaining -= travel

    total_cost = sum(p["cost"] for p in plan)

    return plan, total_cost