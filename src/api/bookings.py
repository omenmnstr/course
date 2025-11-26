from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from schemas.bookings import BookingAddRequest, BookingAdd, BookingResponse
from src.api.dependencies import DBDep, UserIdDep
from repositories.bookings import BookingsRepository

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", response_model=BookingResponse)
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):

    from models.rooms import RoomsOrm
    room_query = select(RoomsOrm).where(RoomsOrm.id == booking_data.room_id)
    room_result = await db.execute(room_query)
    room = room_result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Номер не найден"
        )


    booking_add = BookingAdd(
        user_id=user_id,
        price=room.price,
        **booking_data.model_dump()
    )

    bookings_repo = BookingsRepository(db)
    booking = await bookings_repo.add(booking_add)

    return booking


@router.get("/me", response_model=list[BookingResponse])
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    bookings_repo = BookingsRepository(db)
    bookings = await bookings_repo.get_user_bookings(user_id)
    return bookings


@router.get("", response_model=list[BookingResponse])
async def get_all_bookings(
        db: DBDep,
):
    # if not user.is_admin: ...

    bookings_repo = BookingsRepository(db)
    bookings = await bookings_repo.get_all_bookings()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(
        booking_id: int,
        user_id: UserIdDep,
        db: DBDep,
):
    bookings_repo = BookingsRepository(db)
    booking = await bookings_repo.get_booking_by_id(booking_id)

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено"
        )

    if booking.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому бронированию"
        )

    return booking