from enum import Enum
from typing import Optional, Any

from aiohttp.web_response import json_response, Response

from rest_server.response_codes import HttpResponseCode
from utils import fast_json

SUCCESSFUL_RESPONSE = dict(success=True)
UNSUCCESSFUL_RESPONSE = dict(success=False)
ERROR_RESPONSE = dict(error=True)


class ValidationError(Exception):
    pass


class RestError(Enum):
    NOT_FOUND = "{resource_type} {identifier} does not exists"
    MISSING_ARGUMENT = "Missing {argument} from query"

    def format(self, *args, **kwargs):
        return self.value.format(*args, **kwargs)


def create_success_response(data: Optional[Any] = None,
                            status_code: int = HttpResponseCode.OK) -> Response:
    response_data = SUCCESSFUL_RESPONSE
    if data is not None:
        response_data["data"] = data
    response = json_response(data=response_data, status=status_code, dumps=fast_json.dumps)

    return response


def create_error_response(rest_error: RestError, error_code: int, reason: Optional[str] = None,
                          *args, **kwargs) -> Response:
    response_data = {
        **UNSUCCESSFUL_RESPONSE,
        **ERROR_RESPONSE,
        "description": rest_error.format(*args, **kwargs)
    }
    if reason:
        response_data["reason"] = reason

    return json_response(data=response_data, status=error_code, dumps=fast_json.dumps)
