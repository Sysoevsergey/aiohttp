from aiohttp import web
from aiohttp.typedefs import Handler
from aiohttp.web_exceptions import (
    HTTPInternalServerError,
    HTTPMethodNotAllowed,
    HTTPNotFound,
)

import errors
from models import Session


@web.middleware
async def http_errors_middleware(request: web.Request, handler: Handler):
    try:
        response = await handler(request)
    except HTTPNotFound:
        raise errors.NotFound(description="url not found")
    except HTTPMethodNotAllowed:
        raise errors.MethodNotAllowed(description="method not allowed")
    except HTTPInternalServerError:
        raise errors.UnexpectedError(description="unexpected error")
    return response


@web.middleware
async def session_middleware(request: web.Request, handler: Handler):
    async with Session() as session:
        request["session"] = session
        try:
            response = await handler(request)
            await session.commit()
            return response
        except Exception:
            await session.rollback()
            raise
