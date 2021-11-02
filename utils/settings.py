import re
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseCredentials:
    host: str
    port: int
    password: Optional[str] = None
    username: Optional[str] = None
    db_name: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
REST_PORT = os.getenv("PORT", 5000)

# postgres://<user>:<password>@<host>:<port>/<db_name>
POSTGRES_PATTERN = "postgres://([a-z]*?):(.*?)@(.*?):([0-9]*?)/(.*)"
DATABASE_NAME = "parking"
DATABASE_PASSWORD = "Password1"
LOCAL_POSTGRES_CONFIGURATION = f"postgres://postgres:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}"
DATABASE_URL = os.getenv("DATABASE_URL", LOCAL_POSTGRES_CONFIGURATION)


def get_postgres_credentials() -> DatabaseCredentials:
    result = re.match(POSTGRES_PATTERN, DATABASE_URL)
    username, password, host, port, db_name = result.groups()
    return DatabaseCredentials(username=username,
                               password=password,
                               host=host,
                               port=int(port),
                               db_name=db_name)
