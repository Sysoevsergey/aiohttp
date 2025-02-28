from pydantic import ValidationError

from errors import BadRequest
from schema import SCHEMA_MODEL


def validate(model: SCHEMA_MODEL, data: dict):
    try:
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise BadRequest(error)
