from datetime import datetime
from enum import Enum

import rapidjson


def default(obj):
    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, datetime):
        return obj.isoformat()

    raise TypeError(f"Unable to serialize {obj} (type: {type(obj)})")


def dumps(obj, indent=None) -> str:
    return rapidjson.dumps(obj, datetime_mode=rapidjson.DM_ISO8601, number_mode=rapidjson.NM_NATIVE,
                           default=default, ensure_ascii=False, indent=indent, uuid_mode=rapidjson.UM_CANONICAL)


def loads(deserialized_str: str, support_datetime: bool = False):
    datetime_mode = rapidjson.DM_ISO8601 if support_datetime else rapidjson.DM_NONE
    return rapidjson.loads(deserialized_str, datetime_mode=datetime_mode, number_mode=rapidjson.NM_NATIVE)
