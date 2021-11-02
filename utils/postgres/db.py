import aiopg.sa
import psycopg2
from contextlib import asynccontextmanager

from utils.logging import logger
from utils.settings import get_postgres_credentials

OperationalError = psycopg2.OperationalError
UniqueViolation = psycopg2.errors.UniqueViolation
ForeignKeyViolation = psycopg2.errors.ForeignKeyViolation


class DatabaseConnection:
    _engine = None

    def __init__(self):
        raise RuntimeError("Wrong usage, call get_engine() instead")

    @classmethod
    async def _create_engine(cls):
        postgrs_credentials = get_postgres_credentials()
        return await aiopg.sa.create_engine(host=postgrs_credentials.host,
                                            port=postgrs_credentials.port,
                                            user=postgrs_credentials.username,
                                            password=postgrs_credentials.password,
                                            database=postgrs_credentials.db_name,
                                            echo=True)

    @classmethod
    async def get_engine(cls):
        if not cls._engine:
            try:
                logger.debug("Establishing connection to the database.")
                engine = await cls._create_engine()
                cls._engine = engine
            except OperationalError:
                logger.exception("Establishing database connection error.")

        return cls._engine

    @classmethod
    @asynccontextmanager
    async def acquire_connection(cls):
        engine = await cls.get_engine()
        connection = None

        try:
            connection = await engine.acquire()
            yield connection
        finally:
            if not connection:
                return

            await connection.close()