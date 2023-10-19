# bpl-pyapp-cookiecutter 

A `cookiecutter` template for generating boiler for python postgres projects. 


## features 

__stack__
* py3.11
* postgres 15 - dockerized for local dev

__libs__
* `asyncio`/`anyio` runtime enabled 
* `click` command line interface 
* `sqlalchemy` w/ `asyncpg` database driver 
* `alembic` to handle db migration and versioning 
* `pytest` stack w/ `mypy` and `black` for static type analysis and formatting.
* `fastapi` REST API 
* `pydantic` serde and object mapping 
* `cunybpl/aiodal` - our lightweight asyncpg/sqlalchemy data access layer 
* `cunybpl/auth0_fastapi` - for auth0 integration

## usage 

Install cookiecutter: https://cookiecutter.readthedocs.io/en/stable/index.html


Then just : `$ cookiecutter https://github.com/cunybpl/bpl-pyapp-cookiecutter`

Follow the prompts ...


