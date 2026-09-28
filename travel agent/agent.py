import json
import os

from dotenv import load_dotenv
from groq import Groq

from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.booking_tool import book_trip


# ==================================================
# 1. LOAD ENVIRONMENT
# ==================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")


# ==================================================
# 2. GROQ CLIENT
# ==================================================

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


# ==================================================
# 3. LOAD MEMORY
# ==================================================

def load_memory():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "memory",
        "user_memory.json"
    )

    with open(file_path, "r") as file:
        return json.load(file)


# ==================================================
# 4. UNDERSTAND USER REQUEST
# ==================================================

def understand_request(user_request, memory):

    prompt = f"""
You are a travel planning assistant.

Analyze the user's travel request and return ONLY valid JSON.

User request:
{user_request}

Existing user memory:
{json.dumps(memory, indent=2)}

Return exactly this structure:

{{
    "origin": "city",
    "destination": "city",
    "date": null,
    "duration_days": 3,
    "travelers": 2,
    "budget": 25000,
    "preferred_flight_time": "morning",
    "preferred_hotel_location": "Near Beach",
    "max_hotel_price_per_night": 4500
}}

Rules:

- Extract the origin and destination from the user's request.
- Understand simple requests such as "goa to mumbai".
- Understand natural language such as "i wanna go from goa to mumbai".
- Correct obvious city spelling mistakes when possible.
- Use memory for missing preferences.
- If the user does NOT provide a travel date, return null for date.
- DO NOT invent today's date.
- If the user does not provide a budget, use 25000.
- If the user does not provide number of travelers, use 2.
- If the user does not provide duration, use 3.
- If the user does not provide flight-time preference, use the memory preference.
- If the user does not provide hotel-location preference, use the memory preference.
- If the user does not provide a hotel price limit, use the memory preference.
- Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You extract structured travel requirements."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        include_reasoning=False
    )

    result = response.choices[0].message.content

    return json.loads(result)


# ==================================================
# 5. SEARCH FLIGHTS
# ==================================================

def find_flight(request):

    print("\n🔎 Searching for flights...")

    print(
        f"Route: "
        f"{request['origin']} → "
        f"{request['destination']}"
    )

    if request["date"]:
        print(f"Requested date: {request['date']}")
    else:
        print("Requested date: Not specified")

    print(
        f"Preference: "
        f"{request['preferred_flight_time']}"
    )


    # ==================================================
    # ATTEMPT 1
    # Exact date + preferred flight time
    # ==================================================

    flights = search_flights(
        origin=request["origin"],
        destination=request["destination"],
        date=request["date"],
        morning_only=(
            request["preferred_flight_time"].lower()
            == "morning"
        )
    )

    if flights:
        return flights[0], False


    # ==================================================
    # OBSERVATION
    # ==================================================

    print("\n👀 OBSERVATION:")
    print(
        "No flight matched the requested "
        "route, date and preferences."
    )


    # ==================================================
    # RE-PLANNING 1
    # Relax flight-time preference
    # ==================================================

    print("\n🔄 RE-PLANNING #1:")
    print(
        "Relaxing the morning-flight preference..."
    )

    flights = search_flights(
        origin=request["origin"],
        destination=request["destination"],
        date=request["date"],
        morning_only=False
    )

    if flights:

        print(
            "Found a flight by relaxing "
            "the flight-time preference."
        )

        return flights[0], True


    # ==================================================
    # RE-PLANNING 2
    # Search other available dates
    # ==================================================

    print("\n🔄 RE-PLANNING #2:")
    print(
        "Searching other available dates "
        "for the same route..."
    )

    flights = search_flights(
        origin=request["origin"],
        destination=request["destination"],
        date=None,
        morning_only=False
    )

    if flights:

        selected = flights[0]

        print(
            f"Found an available flight on "
            f"{selected['date']}."
        )

        return selected, True


    # ==================================================
    # FAILURE
    # ==================================================

    print("\n❌ RE-PLANNING FAILED:")
    print(
        "No available flights were found "
        "for this route in the travel dataset."
    )

    return None, True


# ==================================================
# 6. SEARCH HOTELS
# ==================================================

def find_hotel(request):

    print("\n🏨 Searching for hotels...")

    hotels = search_hotels(
        city=request["destination"],
        max_price_per_night=request[
            "max_hotel_price_per_night"
        ],
        location_type=request[
            "preferred_hotel_location"
        ]
    )

    if hotels:
        return hotels[0], False


    print("\n👀 OBSERVATION:")
    print(
        "No hotel matched all the requested "
        "preferences."
    )


    # ==================================================
    # RE-PLANNING 1
    # Increase hotel budget
    # ==================================================

    print("\n🔄 RE-PLANNING #1:")
    print(
        "Relaxing the hotel price constraint..."
    )

    relaxed_price = (
        request["max_hotel_price_per_night"]
        + 1500
    )

    hotels = search_hotels(
        city=request["destination"],
        max_price_per_night=relaxed_price,
        location_type=request[
            "preferred_hotel_location"
        ]
    )

    if hotels:

        print(
            f"New hotel price limit: "
            f"₹{relaxed_price}/night"
        )

        return hotels[0], True


    # ==================================================
    # RE-PLANNING 2
    # Relax hotel location
    # ==================================================

    print("\n🔄 RE-PLANNING #2:")
    print(
        "Relaxing the beach-location preference..."
    )

    hotels = search_hotels(
        city=request["destination"],
        max_price_per_night=relaxed_price
    )

    if hotels:

        print(
            "Found an alternative hotel "
            "in another location."
        )

        return hotels[0], True


    # ==================================================
    # FAILURE
    # ==================================================

    print("\n❌ RE-PLANNING FAILED:")
    print("No suitable hotels found.")

    return None, True


# ==================================================
# 7. CREATE TRAVEL PLAN
# ==================================================

def create_plan(request):

    flight, flight_replanned = find_flight(request)

    if not flight:
        return None


    print(
        f"\n✈️ Selected flight: "
        f"{flight['airline']} "
        f"{flight['departure_time']} "
        f"₹{flight['price']}"
    )


    hotel, hotel_replanned = find_hotel(request)

    if not hotel:
        return None


    print(
        f"\n🏨 Selected hotel: "
        f"{hotel['name']} "
        f"₹{hotel['price_per_night']}/night"
    )


    # ==================================================
    # COST CALCULATION
    # ==================================================

    flight_cost = (
        flight["price"]
        * request["travelers"]
    )

    hotel_nights = (
        request["duration_days"] - 1
    )

    hotel_cost = (
        hotel["price_per_night"]
        * hotel_nights
    )

    total_cost = (
        flight_cost
        + hotel_cost
    )


    print("\n💰 COST CALCULATION")

    print(
        f"Flight cost: ₹{flight_cost}"
    )

    print(
        f"Hotel cost: ₹{hotel_cost}"
    )

    print(
        f"Total cost: ₹{total_cost}"
    )

    print(
        f"Budget: ₹{request['budget']}"
    )


    # ==================================================
    # BUDGET RE-PLANNING
    # ==================================================

    if total_cost > request["budget"]:

        print("\n⚠️ OBSERVATION:")
        print(
            "The selected plan exceeds "
            "the user's budget."
        )

        print("\n🔄 RE-PLANNING:")
        print(
            "Trying to find a cheaper hotel..."
        )

        cheaper_hotels = search_hotels(
            city=request["destination"],
            max_price_per_night=(
                request["budget"]
                // hotel_nights
            )
        )

        if cheaper_hotels:

            hotel = cheaper_hotels[0]

            hotel_cost = (
                hotel["price_per_night"]
                * hotel_nights
            )

            total_cost = (
                flight_cost
                + hotel_cost
            )

            print(
                f"Alternative hotel: "
                f"{hotel['name']}"
            )

            print(
                f"New total cost: "
                f"₹{total_cost}"
            )


    if total_cost > request["budget"]:

        print(
            "\n❌ Unable to create a plan "
            "within budget."
        )

        return None


    return {
        "flight": flight,
        "hotel": hotel,
        "total_cost": total_cost,
        "replanned": (
            flight_replanned
            or hotel_replanned
        )
    }


# ==================================================
# 8. HUMAN APPROVAL
# ==================================================

def ask_for_approval(plan):

    print("\n")
    print("==============================")
    print("        FINAL TRAVEL PLAN")
    print("==============================")


    print(
        f"✈️ Flight: "
        f"{plan['flight']['airline']} "
        f"{plan['flight']['departure_time']}"
    )


    print(
        f"🏨 Hotel: "
        f"{plan['hotel']['name']}"
    )


    print(
        f"💰 Total cost: "
        f"₹{plan['total_cost']}"
    )


    if plan["replanned"]:

        print("\n🔄 NOTE:")
        print(
            "This plan was created "
            "after re-planning."
        )


    print("==============================")


    approval = input(
        "\nDo you approve this booking? (yes/no): "
    )


    return approval.lower() == "yes"


# ==================================================
# 9. MAIN AGENT
# ==================================================

def run_agent():

    print("\n")
    print("================================")
    print("     MINI AUTONOMOUS TRAVEL AGENT")
    print("================================")


    user_request = input(
        "\nWhat trip would you like to plan?\n> "
    )


    memory = load_memory()


    print(
        "\n🧠 Understanding your request..."
    )


    request = understand_request(
        user_request,
        memory
    )


    print(
        "\n📋 Extracted requirements:"
    )


    print(
        json.dumps(
            request,
            indent=2
        )
    )


    print(
        "\n🧠 Creating travel plan..."
    )


    plan = create_plan(request)


    if plan is None:

        print(
            "\n❌ The agent could not create "
            "a suitable plan."
        )

        return


    approved = ask_for_approval(plan)


    if not approved:

        print(
            "\n🛑 Booking cancelled."
        )

        return


    print(
        "\n💳 Processing mock booking..."
    )


    booking = book_trip(
        plan["flight"],
        plan["hotel"],
        user_approved=True
    )


    print("\n")
    print("==============================")
    print("       BOOKING RESULT")
    print("==============================")


    print(
        json.dumps(
            booking,
            indent=2
        )
    )


# ==================================================
# START
# ==================================================

if __name__ == "__main__":
    run_agent()