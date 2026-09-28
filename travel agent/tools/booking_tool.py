import uuid


def book_trip(flight, hotel, user_approved):
    """
    Simulate a travel booking.

    The booking can only happen after explicit
    human approval.
    """

    if not user_approved:
        return {
            "success": False,
            "message": "Booking cancelled because human approval was not provided."
        }

    booking_id = "BOOK-" + str(uuid.uuid4())[:8].upper()

    total_cost = (
        flight["price"] * 2
        + hotel["price_per_night"] * 2
    )

    return {
        "success": True,
        "booking_id": booking_id,
        "flight_id": flight["flight_id"],
        "hotel_id": hotel["hotel_id"],
        "total_cost": total_cost,
        "message": "Mock booking completed successfully."
    }