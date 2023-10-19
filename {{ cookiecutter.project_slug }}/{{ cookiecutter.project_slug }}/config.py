""" Environment variables. The level of granularity is useful for various local and remote configuration.
"""

import os

ENVIRONMENT = os.environ.get(
    "{{ cookiecutter.project_env_prefix}}_ENVIRONMENT", "local"
)
POSTGRES_USER = os.environ.get("{{ cookiecutter.project_env_prefix}}_POSTGRES_USER", "")
POSTGRES_PASSWORD = os.environ.get(
    "{{ cookiecutter.project_env_prefix}}_POSTGRES_PASSWORD", ""
)
POSTGRES_HOST = os.environ.get("{{ cookiecutter.project_env_prefix}}_POSTGRES_HOST", "")
POSTGRES_PORT = os.environ.get("{{ cookiecutter.project_env_prefix}}_POSTGRES_PORT", "")
POSTGRES_DB = os.environ.get("{{ cookiecutter.project_env_prefix}}_POSTGRES_DB", "")

AUTH0_DOMAIN = os.environ.get("{{ cookiecutter.project_env_prefix}}_AUTH0_DOMAIN", "")
AUTH0_AUDIENCE = os.environ.get(
    "{{ cookiecutter.project_env_prefix}}_AUTH0_AUDIENCE", ""
)

MAX_OVERFLOW = os.environ.get(
    "{{ cookiecutter.project_env_prefix}}_DB_ENGINE_MAX_OVERFLOW", 3
)
POOL_SIZE = os.environ.get(
    "{{ cookiecutter.project_env_prefix}}_DB_ENGINE_POOL_SIZE", 3
)
USE_ALEMBIC_URI = os.environ.get(
    "{{ cookiecutter.project_env_prefix}}_USE_ALEMBIC_URI", ""
)


if MAX_OVERFLOW == "":  # pragma: no cover
    MAX_OVERFLOW = 3

if POOL_SIZE == "":  # pragma: no cover
    POOL_SIZE = 3

if USE_ALEMBIC_URI == "":  # pragma: no cover
    USE_ALEMBIC_URI = None

_POSTGRES_URI_BASE = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"

# local -> backend dev
# remote-dev -> frontend dev deployment - allow from localhost or remote
# production -> staging or production - only remote from one of our apps
# testing -> special boi for tests

# NOTE due to bug/weird behavior in starlette we no longer handle CORS in the application
# instead manage this in deployment via nginx ... see:
if ENVIRONMENT == "local":
    # local base url
    POSTGRES_URI = _POSTGRES_URI_BASE + f"{POSTGRES_DB}"
    DEBUG = True

elif ENVIRONMENT == "production":
    # ssl no debug
    POSTGRES_URI = _POSTGRES_URI_BASE + f"{POSTGRES_DB}?ssl=require"
    DEBUG = False

# NOTE this is to hack our way through dealing with alembic in a test environment... :((
elif ENVIRONMENT == "testing":
    POSTGRES_TEST_DB = os.environ.get(
        "{{ cookiecutter.project_env_prefix}}_POSTGRES_TEST_DB", default="testdb"
    )
    POSTGRES_URI = _POSTGRES_URI_BASE + f"{POSTGRES_TEST_DB}"
    DEBUG = True

else:
    raise ValueError("ENVIRONMENT must be either local, testing  or production")
