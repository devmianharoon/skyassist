from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select
from datetime import datetime
from typing import List, Optional
import calendar
from app.config import engine
from app.models.flight_model import Flight, FlightLocation
# Define the app
app = FastAPI()



# Models




# Create tables in the database
SQLModel.metadata.create_all(engine)

# Create a helper function to get the day of the week
def get_day_of_week(date: datetime) -> str:
    return calendar.day_name[date.weekday()]

# API to add a flight
@app.post("/flights/")
async def add_flight(flight_number: str, departure_time: datetime, arrival_time: datetime, from_location: str, to_location: str):
    with Session(engine) as session:
        # Get or create locations
        from_location_db = session.exec(select(FlightLocation).filter(FlightLocation.LocationName == from_location)).first()
        if not from_location_db:
            from_location_db = FlightLocation(LocationName=from_location)
            session.add(from_location_db)
            session.commit()
            session.refresh(from_location_db)
        
        to_location_db = session.exec(select(FlightLocation).filter(FlightLocation.LocationName == to_location)).first()
        if not to_location_db:
            to_location_db = FlightLocation(LocationName=to_location)
            session.add(to_location_db)
            session.commit()
            session.refresh(to_location_db)
        
        # Create flight record
        day_of_week = get_day_of_week(departure_time)
        
        flight = Flight(
            FlightNumber=flight_number,
            DepartureTime=departure_time,
            ArrivalTime=arrival_time,
            FromLocationID=from_location_db.LocationID,
            ToLocationID=to_location_db.LocationID,
            DayOfWeek=day_of_week
        )
        
        session.add(flight)
        session.commit()
        session.refresh(flight)
        
        return {"message": "Flight added successfully", "flight_id": flight.FlightID, "day_of_week": day_of_week}

# API to list all flights
@app.get("/flights/", response_model=List[Flight])
async def get_flights():
    with Session(engine) as session:
        flights = session.exec(select(Flight)).all()
        return flights
