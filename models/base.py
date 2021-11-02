from typing import Dict, List, Union, Type

from sqlalchemy import Column, Enum
from sqlalchemy.ext.declarative import declarative_base


class MissingNotNullableValue(Exception):
    pass


def parse_enum_value(enum_type: Type[Enum], value: Union[str, int, Enum]):
    if isinstance(value, enum_type):
        return value

    try:
        return enum_type[value.upper()]
    except ValueError:
        return enum_type[int(value)]  # In case of IntEnum


def serialize_value(column: Column, value: any):
    column_type = column.type
    if isinstance(column_type, Enum):
        return parse_enum_value(column_type.enum_class, value)

    return value


def declarative_constructor(self, **kwargs):
    for column in self.columns:
        column_name = column.name

        if not column.nullable and column_name not in kwargs:
            raise MissingNotNullableValue(f"Value for {column_name} is not specified")

        value = kwargs.get(column_name)
        setattr(self, column_name, serialize_value(column, value))


class Base:
    @property
    def columns(self) -> List[Column]:
        return list(self.__table__.columns)

    def to_json(self) -> Dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.columns
        }


Model = declarative_base(cls=Base, constructor=declarative_constructor)