import json
from aiohttp import web
from pydantic import ValidationError

from models import engine, Base, Session, Ad
from sqlalchemy.exc import IntegrityError

from schema import VALIDATION_CLASS, CreateAd, PatchAd


async def orm_context(app):
    print("START")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('SHUT DOWN')


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict
async def get_ad(session: Session, ad_id: int) -> Ad:
    ad = await session.get(Ad, ad_id)
    if ad is None:
        raise web.HTTPNotFound(
            text=json.dumps({'error': "ad doesn't exist"}),
            content_type='application/json'
        )
    return ad


class AdView(web.View):

    async def get(self, ad_id: int):
        with Session() as session:
            ad = await get_ad(session, ad_id)
            return web.json_response(
                {
                    "id": ad.id,
                    "title": ad.title,
                    "description": ad.description,
                    "owner": ad.owner,
                    "creation_date": int(ad.creation_date.timestamp()),
                }
            )

    async def post(self):
        json_data = await validate_json(self.request.json, CreateAd)
        with Session() as session:
            ad = Ad(**json_data)
            session.add(ad)
            try:
                await session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["title"]} с таким заголовком уже есть')
            return web.json_response({"id": ad.id})


    async def patch(self, ad_id: int):
        json_data = validate_json(self.request.json, PatchAd)
        with Session() as session:
            ad = await get_ad(session, ad_id)
            for field, value in json_data.items():
                setattr(ad, field, value)
            session.add(ad)
            try:
                await session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["title"]} с таким заголовком уже есть')
            return web.json_response(
                {
                    "id": ad.id,
                    "title": ad.title,
                    "description": ad.description,
                    "owner": ad.owner,
                    "creation_date": ad.creation_date,
                    # .isoformat(timespec='hours')
                }
            )

    async def delete(self, ad_id: int):
        with Session() as session:
            ad = await get_ad(session, ad_id)
            await session.delete(ad)
            await session.commit()
            return web.json_response({"status": "success"})


async def get_app():
    app = web.Application()
    app.add_routes(
        [
            web.get("/ad/{ad_id:\d+}", AdView),
            web.patch("/ad/{ad_id:\d+}", AdView),
            web.delete("/ad/{ad_id:\d+}", AdView),
            web.post("/ad/", AdView),
        ]
    )

    app.cleanup_ctx.append(orm_context)
    app.middlewares.append(session_middleware)

    return app


if __name__ == '__main__':
    app = get_app()
    web.run_app(app)
