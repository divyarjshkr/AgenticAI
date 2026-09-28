import json
import os


def search_flights(
    origin,
    destination,
    date=None,
    max_price=None,
    morning_only=False
):
    """
    Search available flights from the JSON dataset.
    """

    file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "flights.json"
    )

    with open(file_path, "r") as file:
        flights = json.load(file)

    results = []

    for flight in flights:

        if not flight["available"]:
            continue

        if flight["origin"].lower() != origin.lower():
            continue

        if flight["destination"].lower() != destination.lower():
            continue

        if date and flight["date"] != date:
            continue

        if max_price and flight["price"] > max_price:
            continue

        if morning_only:

            hour = int(
                flight["departure_time"]
                .split(":")[0]
            )

            if hour >= 12:
                continue

        results.append(flight)


    results.sort(
        key=lambda x: (
            x["price"],
            x["date"],
            x["departure_time"]
        )
    )


    return results