
import os
import time
import asyncio

import uvloop
from asyncpg import connect, create_pool

from sanic import Sanic
from sanic.response import json, text
import psycopg2.pool

def jsonify(records):
    return [dict(r.items()) for r in records]

app = Sanic(__name__)

TEST_SQL_QUERY = 'SELECT * FROM data;'
DSN = 'postgres://arellok:test@127.0.0.1/test_async'

@app.listener('before_server_start')
async def register_db(app, loop):
    app.pool_1 = await create_pool(
            DSN, loop=loop, min_size=10, max_size=100)
    #app.pool_2 = psycopg2.pool.PersistentConnectionPool(
    #        dsn=DSN, minconn=10, maxconn=10)
    async with app.pool_1.acquire() as connection:
        await connection.execute('DROP TABLE IF EXISTS data')
        await connection.execute("""CREATE TABLE data (
                                id serial primary key,
                                content varchar(50),
                                post_date timestamp
                            );""")
        for i in range(0, 1000):
            await connection.execute(f"""INSERT INTO data
                (id, content, post_date) VALUES ({i}, {i}, now())""")

@app.get('/asyncpg/select')
async def root_get(request):
    #start = time.monotonic()
    async with app.pool_1.acquire() as connection:
        results = await connection.fetch(TEST_SQL_QUERY)
        payload = {'posts': jsonify(results)}
    #end = time.monotonic()
    #print (end - start)
    return json(payload)

@app.get('/psycopg2/select')
async def psycopg2_select(request):
    start = time.monotonic()
    conn = app.pool_2.getconn()
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute(TEST_SQL_QUERY)
        columns = [x.name for x in curs.description]
        results = curs.fetchall()
    payload = {'posts': [{x: y for x, y in zip(columns, result)} for result in results]}
    end = time.monotonic()
    print (end - start)
    return json(payload)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
