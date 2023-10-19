import click
import asyncio

from aiodal import connect
from sqlalchemy import make_url, URL
import sqlalchemy as sa

from .. import config


def _parse_uri(uri: str | None) -> URL | None:
    if uri:
        uri = "postgresql+asyncpg://" + uri.split("://")[-1] if "://" in uri else uri
        return make_url(uri)
    return None


_uri_help = """ 
A valid postgres uri similar to `psql` format: postgresql://username:password@host:port/db[?ssl=require].
If not supplied will instead rely on environment variables that construct `config.POSTGRES_URI`.
"""


@click.group("{{ cookiecutter.project_slug }}")
@click.pass_context
@click.option(
    "-u",
    "--uri",
    type=click.STRING,
    default=None,
    help=_uri_help,
)
def main(ctx: click.Context, uri: str | None) -> None:
    """{{  cookiecutter.project_slug }} cli."""

    ctx.ensure_object(dict)
    if uri:
        ctx.obj["uri"] = _parse_uri(uri)
    else:
        ctx.obj["uri"] = config.POSTGRES_URI


@main.command("check")
@click.pass_context
def check(ctx: click.Context) -> None:
    """Ping postgres db for connectivity."""

    async def try_connect() -> None:
        db = await connect.or_fail(ctx.obj["uri"])

        async with db.engine.connect() as conn:
            await conn.execute(sa.text("select 1"))

        await db.engine.dispose()

    asyncio.run(try_connect())
    print("Connect Ok")
