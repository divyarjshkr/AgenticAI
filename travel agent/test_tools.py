from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels


print("\n===== FLIGHT SEARCH =====")

flights = search_flights(
    origin="Bengaluru",
    destination="Goa",
    date="2026-10-10",
    max_price=5000,
    morning_only=True
)

for flight in flights:
    print(
        flight["flight_id"],
        "|",
        flight["airline"],
        "|",
        flight["departure_time"],
        "| ₹" + str(flight["price"])
    )


print("\n===== HOTEL SEARCH =====")

hotels = search_hotels(
    city="Goa",
    max_price_per_night=4500,
    location_type="Near Beach"
)

for hotel in hotels:
    print(
        hotel["hotel_id"],
        "|",
        hotel["name"],
        "|",
        hotel["location_type"],
        "| ₹" + str(hotel["price_per_night"]),
        "| Rating:",
        hotel["rating"]
    )