from datetime import datetime
from typing import Optional
from sqlmodel import Session
from app.models.flight_model import Booking, Cancellation, Flight
from sqlmodel import Session, select
from app.config import engine
from app.ai.rag import info_retriever
from app.ai.llm import llm


def book_flight(user_id: int, flight_id: int, passenger_name: str):
    """
    Books a flight for a user.

    Args:
        user_id (int): The ID of the user making the booking.
        flight_id (int): The ID of the flight to be booked.
        passenger_name (str): The name of the passenger making the booking.

    Returns:
        str: A confirmation message including the booking ID or an error message if the flight is not found.
    """
    with Session(engine) as session:
        # Check if the flight exists
        flight = session.exec(
            select(Flight).where(Flight.FlightID == flight_id)
        ).first()
        if not flight:
            return "Flight not found."

        # Create a new booking
        booking = Booking(
            UserID=user_id,
            FlightID=flight_id,
            PassengerName=passenger_name,
            BookingDate=datetime.utcnow(),
            Status="Booked",
        )

        session.add(booking)
        session.commit()
        session.refresh(booking)
        return f"Booking successful: {booking.BookingID}"


def cancel_booking(user_id: int, booking_id: int, reason: Optional[str] = None):
    """
    Cancels an existing booking.

    Args:
        user_id (int): The ID of the user requesting the cancellation.
        booking_id (int): The ID of the booking to be cancelled.
        reason (Optional[str]): The reason for cancellation (optional).

    Returns:
        str: A confirmation message including the cancellation ID or an error message if the booking is not found.
    """
    with Session(engine) as session:
        # Check if the booking exists
        booking = session.exec(
            select(Booking).where(
                Booking.BookingID == booking_id, Booking.UserID == user_id
            )
        ).first()
        if not booking:
            return "Booking not found or not associated with the user."

        # Create a cancellation record
        cancellation = Cancellation(
            BookingID=booking.BookingID,
            UserID=user_id,
            CancellationDate=datetime.utcnow(),
            Reason=reason,
        )

        session.add(cancellation)
        session.commit()
        session.refresh(cancellation)
        return f"Cancellation successful: {cancellation.CancellationID}"


def get_all_flights():
    """
    Fetches all available flights.

    Returns:
        list: A list of flight details, including flight number, departure time, arrival time, and locations.
    """
    with Session(engine) as session:
        flights = session.exec(select(Flight)).all()
        if not flights:
            return "No flights available."

        flight_list = []
        for flight in flights:
            flight_list.append(
                {
                    "FlightNumber": flight.FlightNumber,
                    "DepartureTime": flight.DepartureTime,
                    "ArrivalTime": flight.ArrivalTime,
                    "FromLocation": flight.from_location.LocationName,
                    "ToLocation": flight.to_location.LocationName,
                    "Status": flight.FlightStatus,
                }
            )
        return flight_list


def get_user_bookings(user_id: int):
    """
    Retrieves all bookings associated with a user.

    Args:
        user_id (int): The ID of the user for whom the bookings are to be fetched.

    Returns:
        list: A list of bookings, including booking ID, flight details, and booking status.
    """
    with Session(engine) as session:
        # Query the bookings associated with the user
        bookings = session.exec(select(Booking).where(Booking.UserID == user_id)).all()

        if not bookings:
            return "No bookings found for this user."

        booking_list = []
        for booking in bookings:
            flight = session.exec(
                select(Flight).where(Flight.FlightID == booking.FlightID)
            ).first()
            flight_info = {
                "FlightNumber": flight.FlightNumber,
                "DepartureTime": flight.DepartureTime,
                "ArrivalTime": flight.ArrivalTime,
                "FromLocation": flight.from_location.LocationName,
                "ToLocation": flight.to_location.LocationName,
                "Status": flight.FlightStatus,
            }
            booking_list.append(
                {
                    "BookingID": booking.BookingID,
                    "PassengerName": booking.PassengerName,
                    "BookingDate": booking.BookingDate,
                    "Status": booking.Status,
                    "FlightInfo": flight_info,
                }
            )

        return booking_list


# Array of Tools
all_tools = [
    book_flight,
    cancel_booking,
    get_all_flights,
    get_user_bookings,
    info_retriever,
]

# Bind All Tools With LLM

llm_with_tools = llm.bind_tools(all_tools)
