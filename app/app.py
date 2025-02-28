from aiohttp import web
from middleware import http_errors_middleware, session_middleware
from server import orm_context
from server import UserView, AdvertisementView


def _get_app() -> web.Application:
    app = web.Application()
    app.middlewares.extend([http_errors_middleware, session_middleware])
    app.cleanup_ctx.append(orm_context)

    app.add_routes([
        web.post("/user", UserView),
        web.get("/user/{user_id:[0-9]+}", UserView),
        web.patch("/user/{user_id:[0-9]+}", UserView),
        web.delete("/user/{user_id:[0-9]+}", UserView),

        web.post('/advertisement', AdvertisementView),
        web.get('/advertisement/{advertisement_id:[0-9]+}', AdvertisementView),
        web.patch('/advertisement/{advertisement_id:[0-9]+}', AdvertisementView),
        web.delete('/advertisement/{advertisement_id:[0-9]+}', AdvertisementView),
    ])

    return app

async def get_app():
    return _get_app()


if __name__ == "__main__":
    web.run_app(_get_app())
