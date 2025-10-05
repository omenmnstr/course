from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.users import UsersOrm
from repositories.base import BaseRepository
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def create_user(self, user_data):
        try:
            db_user = self.model(**user_data.model_dump())

            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)

            return self.schema.model_validate(db_user)

        except IntegrityError as e:
            await self.session.rollback()

            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists"
                )



