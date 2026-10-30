
"""Flight reservation system with improved security and code quality."""

import hashlib
import json
import os
import secrets
from pathlib import Path

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

REVENUE = {"total": 0.0}


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Book a seat and record the passenger's baggage details."""
    if baggage_tags is None:
        baggage_tags = []

    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False

    FLIGHTS[flight_no]["seats"] -= 1

    if FLIGHTS[flight_no]["seats"] <= 0:
        FLIGHTS[flight_no]["is_full"] = True

    REVENUE["total"] += FLIGHTS[flight_no]["fare"]

    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger "
        f"{passenger} with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel a booking and restore one available seat."""
    if flight_no not in FLIGHTS:
        return False

    FLIGHTS[flight_no]["seats"] += 1
    FLIGHTS[flight_no]["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Check whether a flight has available seats."""
    flight = FLIGHTS.get(flight_no)
    return flight is not None and not flight["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate=0.15):
    """Calculate the baggage surcharge using a safe numeric rate."""
    if flight_no not in FLIGHTS:
        raise ValueError(f"Unknown flight number: {flight_no}")

    if not 0 <= surcharge_rate <= 1:
        raise ValueError("Surcharge rate must be between 0 and 1.")

    base_fare = FLIGHTS[flight_no]["fare"]
    return base_fare * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Generate a SHA-256 hash for a passenger ID."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a cryptographically secure four-digit boarding PIN."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.txt"):
    """Export flight details to a JSON-formatted manifest file."""
    manifest = json.dumps(FLIGHTS, indent=4)
    Path(filename).write_text(manifest, encoding="utf-8")


def get_flight_summary(flight_data):
    """Return the number of flights with available seats."""
    return sum(
        not flight["is_full"] for flight in flight_data.values()
    )


def main():
    """Run the flight reservation system demonstration."""
    airline_api_secret = os.getenv("AIRLINE_API_SECRET")

    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")

    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101"))
    print(
        "Passenger Hash:",
        generate_passenger_hash("SAMPLE_PASSENGER_ID"),
    )
    print("Boarding PIN:", generate_boarding_pin())

    export_flight_manifest()

    print("Available flights:", get_flight_summary(FLIGHTS))
    print("Total Revenue:", REVENUE["total"])
    print("API Token configured:", bool(airline_api_secret))


if __name__ == "__main__":
    main()
