import asyncio
from functools import partial
from asyncpg import create_pool
from sanic import Blueprint


bp = Blueprint('dp')


async def _pg_fetch(pg_pool, sql, *args, **kwargs):
    async with pg_pool.acquire() as connection:
        return await connection.fetch(sql, *args, **kwargs)


async def _pg_execute(pg_pool, sql, *args, **kwargs):
    async with pg_pool.acquire() as connection:
        return await connection.execute(sql, *args, **kwargs)


class PG:
    def __init__(self, pg_pool):
        self.fetch = partial(_pg_fetch, pg_pool)
        self.execute = partial(_pg_execute, pg_pool)


@bp.listener('before_server_start')
async def init_pg(app, loop):
    #print (app.config.PG_CFG)
    app.pg_pool = await create_pool(
        **app.db,
        #dsn='postgres://arellok:test@127.0.0.1:5432/test_async',
        loop=loop,
        max_size=100,
    )
    app.pg = PG(app.pg_pool)
