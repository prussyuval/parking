from enum import IntEnum


class Status(IntEnum):
    unknown = 0
    empty = 1
    few_left = 2
    full = 3


STATUS_NAMING_MAP = {
    Status.empty: "EMPTY",
    Status.few_left: "FEW_LEFT",
    Status.full: "FULL",
}

STATUS_TO_SCORE = {
    Status.empty: 0,
    Status.few_left: 99,
    Status.full: 100,
}
