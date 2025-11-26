from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

class Booking(BookingAdd):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
