from models.bookings import BookingsOrm
from schemas.bookings import Booking
from src.repositories.base import BaseRepository

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_user_bookings(self, user_id: int) -> list[Booking]:
        return await self.get_filtered(user_id=user_id)

    async def get_all_bookings(self) -> list[Booking]:
        return await self.get_all()

    async def get_booking_by_id(self, booking_id: int) -> Booking | None:
        return await self.get_one_or_none(id=booking_id)

