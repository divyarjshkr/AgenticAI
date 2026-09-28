import json
import os


def search_hotels(
    city,
    max_price_per_night=None,
    location_type=None,
    min_rating=None
):
    """
    Search available hotels from the JSON dataset.
    """

    file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "hotels.json"
    )

    with open(file_path, "r") as file:
        hotels = json.load(file)

    results = []

    for hotel in hotels:

        if not hotel["available"]:
            continue

        if hotel["rooms_available"] <= 0:
            continue

        if hotel["city"].lower() != city.lower():
            continue

        if max_price_per_night:
            if hotel["price_per_night"] > max_price_per_night:
                continue

        if location_type:
            if hotel["location_type"].lower() != location_type.lower():
                continue

        if min_rating:
            if hotel["rating"] < min_rating:
                continue

        results.append(hotel)

    results.sort(
        key=lambda x: (
            x["price_per_night"],
            -x["rating"]
        )
    )

    return results