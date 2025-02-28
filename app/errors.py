import json
from aiohttp.web import HTTPException


class Error(HTTPException):
    def __init__(self, description: dict | list | str):
        self.description = description

        super().__init__(
            text=json.dumps({"status": "error", "description": description}),
            content_type="application/json",
        )


class NotFound(Error):
    status_code = 404


class BadRequest(Error):
    status_code = 400


class Conflict(Error):
    status_code = 409


class Unauthorized(Error):
    status_code = 401


class Forbidden(Error):
    status_code = 403


class MethodNotAllowed(Error):
    status_code = 405


class UnexpectedError(Error):
    status_code = 500