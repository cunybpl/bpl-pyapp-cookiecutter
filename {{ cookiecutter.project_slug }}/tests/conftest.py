import pathlib
from {{ cookiecutter.project_slug }} import config 
import pytest
from aiodal import dal

import os

this_dir = pathlib.Path(__file__).parent
root_dir = this_dir.parent

from {{ cookiecutter.project_slug }} import config


from basatdb.api.base import orjson_serializer

import logging

# turning off httpx annyoing ass logger
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# configure this seperately so we can connect and create a database first.
if config.ENVIRONMENT != "testing":
    raise ValueError(
        "must set environment variable to `testing` in order to correctly configure test suite"
    )


# need this to keep event loop for the duration of the tests
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def engine_uri():
    return config.POSTGRES_URI


@pytest.fixture
async def module_transaction(db):
    """auto rollback. Module level isolation"""
    async with db.engine.connect() as conn:
        transaction = dal.TransactionManager(conn, db)
        try:
            yield transaction
        finally:
            await transaction.rollback()

@pytest.fixture(scope="module")
async def module_transaction(db):
    """auto rollback. Module level isolation"""
    async with db.engine.connect() as conn:
        transaction = dal.TransactionManager(conn, db)
        try:
            yield transaction
        finally:
            await transaction.rollback()
