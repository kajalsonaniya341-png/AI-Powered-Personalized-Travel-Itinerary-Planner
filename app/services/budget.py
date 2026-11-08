"""Full trip cost estimator: stay + food + local transport + travel to the destination + entry fees + extras.

HONESTY: there is no live price data here. The rates below are rough planning figures (INR) chosen by
travel style and destination type. They are ESTIMATES to help you plan, not quotes. Replace RATES with
your own research for better accuracy. Only "travel to destination" is something YOU enter.

All amounts are for the WHOLE group unless a label says "per person".
"""
import math

# (room per night for up to 2 people, food per person per day, local transport per vehicle per day)
RATES = {
    "budget":   {"metro": (1800, 400, 400),  "tourist": (1500, 350, 350),  "standard": (1000, 300, 300)},
    "balanced": {"metro": (3500, 800, 900),  "tourist": (3000, 700, 800),  "standard": (2000, 550, 600)},
    "luxury":   {"metro": (9000, 2000, 2500), "tourist": (8000, 1800, 2200), "standard": (5000, 1200, 1500)},
}
METRO = {"Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune"}
TOURIST = {"Jaipur", "Udaipur", "Jaisalmer", "Pushkar", "Goa", "Kochi", "Munnar", "Alleppey", "Agra", "Varanasi",
           "Rishikesh", "Shimla", "Manali", "Srinagar", "Gulmarg", "Pahalgam", "Leh", "Darjeeling", "Ooty", "Hampi",
           "Mysuru", "Puducherry", "Port Blair", "Gangtok", "Khajuraho", "Mahabalipuram", "Coorg", "Dharamshala",
           "Nainital", "Mussoorie", "Haridwar", "Jodhpur", "Amritsar", "Puri", "Tawang", "Cherrapunji", "Kaziranga"}
PEOPLE_PER_ROOM = 2
PEOPLE_PER_VEHICLE = 4
EXTRAS_RATE = 0.10
STYLES = ("budget", "balanced", "luxury")
LABELS = {"budget": "Budget", "balanced": "Balanced", "luxury": "Luxury"}
MODE_LABELS = {"flight": "flight", "train": "train", "bus": "bus", "car": "own car"}


def destination_tier(city: str) -> str:
    return "metro" if city in METRO else "tourist" if city in TOURIST else "standard"


def estimate_trip_cost(city: str, days: int, travelers: int, travel_style: str, entry_fees_total: float,
                       nights: int | None = None, travel_cost_per_person: float = 0.0, budget: float | None = None,
                       travel_mode: str = "none") -> dict:
    """Return a full cost breakdown (all numbers are estimates)."""
    style = travel_style if travel_style in RATES else "balanced"
    tier = destination_tier(city)
    nights = max(days - 1, 0) if nights is None else nights
    room, food_pp, vehicle_day = RATES[style][tier]
    rooms = math.ceil(travelers / PEOPLE_PER_ROOM)
    vehicles = math.ceil(travelers / PEOPLE_PER_VEHICLE)

    rows = [
        ("stay", "Stay", rooms * nights * room,
         f"{rooms} room{'s' if rooms > 1 else ''} x {nights} night{'s' if nights != 1 else ''} x ₹{room:,}"),
        ("food", "Food", travelers * days * food_pp, f"{travelers} traveler{'s' if travelers > 1 else ''} x {days} day{'s' if days > 1 else ''} x ₹{food_pp:,}"),
        ("local_transport", "Local transport", vehicles * days * vehicle_day,
         f"{vehicles} vehicle{'s' if vehicles > 1 else ''} x {days} day{'s' if days > 1 else ''} x ₹{vehicle_day:,}"),
        ("entry_fees", "Attraction entry fees", entry_fees_total, "From your itinerary (cost per person x travelers)"),
        ("travel_to", "Travel to destination (round trip)" + (f" by {MODE_LABELS[travel_mode]}" if travel_mode in MODE_LABELS else ""), travel_cost_per_person * travelers,
         (f"₹{travel_cost_per_person:,.0f} per person x {travelers}" if travel_cost_per_person
          else "Not included: enter your ticket or fuel and toll cost to add it")),
    ]
    subtotal = sum(r[2] for r in rows)
    extras = round(subtotal * EXTRAS_RATE)
    rows.append(("extras", "Extras and buffer (10%)", extras, "Shopping, tips, small purchases, price changes"))
    total = round(subtotal + extras)

    result = {
        "breakdown": [{"key": k, "label": l, "amount": round(a), "basis": b} for k, l, a, b in rows],
        "total": total, "per_person": round(total / travelers), "per_day": round(total / max(days, 1)),
        "nights": nights, "tier": tier, "style": style, "travel_mode": travel_mode,
        "assumptions": [f"{PEOPLE_PER_ROOM} travelers share a room; {PEOPLE_PER_VEHICLE} travelers per cab/auto.",
                        f"Rates are rough {LABELS[style].lower()}-style estimates for a {tier} destination, not live prices.",
                        "Hotel, food and transport prices change with season and availability; check before booking."],
    }
    if budget is not None:
        result["budget"] = budget
        result["within_budget"] = total <= budget
        result["difference"] = round(abs(budget - total))
    return result


def style_alternatives(city: str, days: int, travelers: int, entry_fees_total: float,
                       nights: int | None = None, travel_cost_per_person: float = 0.0) -> dict:
    """Total cost under each travel style (entry fees held the same), to show what fits the budget."""
    return {s: estimate_trip_cost(city, days, travelers, s, entry_fees_total, nights, travel_cost_per_person)["total"]
            for s in STYLES}
