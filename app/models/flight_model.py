from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date, datetime

# User Table
class User(SQLModel, table=True):
    __tablename__ = 'user'
    
    UserID: int = Field(default=None, primary_key=True)
    UserName: str
    Email: str
    password: str
    Phone: Optional[str] = None
    # Relationships
    bookings: List["Booking"] = Relationship(back_populates="user")
    cancellations: List["Cancellation"] = Relationship(back_populates="user")


# Flight Location Table
class FlightLocation(SQLModel, table=True):
    __tablename__ = 'flight_location'
    
    LocationID: int = Field(default=None, primary_key=True)
    LocationName: str = Field(index=True)
    
    flights_from: List["Flight"] = Relationship(back_populates="from_location")
    flights_to: List["Flight"] = Relationship(back_populates="to_location")



# Flight Table
class Flight(SQLModel, table=True):
    __tablename__ = 'flight'
    
    FlightID: int = Field(default=None, primary_key=True)
    FlightNumber: str
    DepartureTime: datetime
    ArrivalTime: datetime
    FromLocationID: int = Field(foreign_key="flight_location.LocationID")
    ToLocationID: int = Field(foreign_key="flight_location.LocationID")
    FlightStatus: str = Field(default="Scheduled")
    DayOfWeek: str  # Stores the day of the week (e.g., "Monday")
    
    from_location: FlightLocation = Relationship(back_populates="flights_from")
    to_location: FlightLocation = Relationship(back_populates="flights_to")



# Booking Table
class Booking(SQLModel, table=True):
    __tablename__ = 'booking'
    
    BookingID: int = Field(default=None, primary_key=True)
    FlightID: int = Field(foreign_key="flight.FlightID")
    UserID: int = Field(foreign_key="user.UserID")  # Foreign key to User table
    PassengerName: str
    BookingDate: datetime = Field(default_factory=datetime.utcnow)
    Status: str = Field(default="Booked")
    
    # Relationships
    flight: Flight = Relationship(back_populates="bookings")
    user: User = Relationship(back_populates="bookings")
    cancellations: List["Cancellation"] = Relationship(back_populates="booking")


# Cancellation Table
class Cancellation(SQLModel, table=True):
    __tablename__ = 'cancellation'
    
    CancellationID: int = Field(default=None, primary_key=True)
    BookingID: int = Field(foreign_key="booking.BookingID")
    UserID: int = Field(foreign_key="user.UserID")  # Foreign key to User table
    CancellationDate: datetime = Field(default_factory=datetime.utcnow)
    Reason: Optional[str] = None
    
    # Relationships
    booking: Booking = Relationship(back_populates="cancellations")
    user: User = Relationship(back_populates="cancellations")
