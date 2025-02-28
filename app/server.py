from typing import Type
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from models import init_orm, close_orm
from sqlalchemy.exc import IntegrityError
import json

from auth import hash_password
from models import Advertisement, User, engine, Base
from schema import CreateAdvertisement, UpdateAdvertisement
from tools import validate


def get_http_error(err_cls, message: str | dict | list):
    error_message = json.dumps({"error": message})
    return err_cls(text=error_message, content_type="application/json")

app = web.Application()


async def orm_context(app: web.Application):
    print("start")
    await init_orm()
    yield
    print("finish")
    await close_orm()



async def get_user_by_id(user_id: int, session: AsyncSession) -> Type[User]:
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, "user not found")
    return user

async def add_user(user: User, session: AsyncSession):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, "user already exist")

async def delete_user(user: User, session: AsyncSession):
    await session.delete(user)
    await session.commit()


class UserView(web.View):

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        session = self.request["session"]
        user = await get_user_by_id(self.user_id, session)
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        json_data['password'] = hash_password(json_data['password'])
        user = User(**json_data)
        session = self.request["session"]
        await add_user(user, session)
        return web.json_response(user.dict)

    async def patch(self):
        json_data = await self.request.json()
        session = self.request["session"]
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        user = await get_user_by_id(self.user_id, session)
        for field, value in json_data.items():
            setattr(user, field, value)
        await add_user(user, session)
        return web.json_response(user.dict)

    async def delete(self):
        session = self.request["session"]
        user = await get_user_by_id(self.user_id, session)
        await delete_user(user, session)
        return web.json_response({'status': 'deleted'})


async def get_advertisement_by_id(advertisement_id: int, session: AsyncSession) -> Type[Advertisement]:
    advertisement = await session.get(Advertisement, advertisement_id)
    if not advertisement:
        raise get_http_error(web.HTTPNotFound, "Advertisement not found")
    return advertisement

async def add_advertisement(advertisement: Advertisement, session: AsyncSession):
    session.add(advertisement)
    try:
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, "Advertisement already exists")

async def delete_advertisement(advertisement: Advertisement, session: AsyncSession):
    await session.delete(advertisement)
    await session.commit()


class AdvertisementView(web.View):

    @property
    def advertisement_id(self) -> int:
        return int(self.request.match_info["advertisement_id"])

    async def get(self):
        session = self.request["session"]
        advertisement = await get_advertisement_by_id(self.advertisement_id, session)
        return web.json_response(advertisement.dict)

    async def post(self):
        json_data = await self.request.json()
        session = self.request["session"]
        valid_data = validate(CreateAdvertisement, json_data)
        advertisement = Advertisement(**valid_data)
        await add_advertisement(advertisement, session)
        return web.json_response(advertisement.dict)

    async def patch(self):
        json_data = await self.request.json()
        session = self.request["session"]
        valid_data = validate(UpdateAdvertisement, json_data)
        advertisement = await get_advertisement_by_id(self.advertisement_id, session)
        for field, value in valid_data.items():
            setattr(advertisement, field, value)
        await session.commit()
        return web.json_response(advertisement.dict)

    async def delete(self):
        session = self.request["session"]
        advertisement = await get_advertisement_by_id(self.advertisement_id, session)
        await delete_advertisement(advertisement, session)
        return web.json_response({"status": "deleted"})
