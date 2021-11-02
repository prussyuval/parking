from enum import IntEnum


class Status(IntEnum):
    unknown = 0
    empty = 1
    few_left = 2
    full = 3