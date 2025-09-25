from fastapi import Query, APIRouter, Body
from sqlalchemy.ext.asyncio import async_sessionmaker
from  sqlalchemy import insert, select, func
from database import async_session_maker, engine
from models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])





@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Город"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit = per_page,
            offset=per_page * (pagination.page-1))

    #per_page = pagination.per_page or 5
    #async with async_session_maker() as session:
       #query = select(HotelsOrm)
        #if location:
        #    query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
       # if title:
       #     query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        #query = (
       #     query
        #    .limit(per_page)
       #     .offset (per_page * (pagination.page-1))
       # )
        #result = await session.execute(query)
        #hotels = result.scalars().all()


    # if pagination.page and pagination.per_page:
        #return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]



@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {},
    "2": {}
})
):
    async with async_session_maker() as session:
       hotel = await HotelsRepository(session).add(hotel_data)
       await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
