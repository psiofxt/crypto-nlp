from sanic import Sanic, response
import sys
from jinja2 import Environment, PackageLoader, select_autoescape
import json
from db import bp
import psycopg2
from asyncpg import create_pool

def error_response(errors, status=None):
    error_data = []
    if not status:
        status = errors[0]['status']
    for error in errors:
        error_data.append({k: error[k] for k in ('code', 'message')})
    return response.json({'errors': error_data}, status=status)


MISSING_FIELDS = {'code': 100, 'message': 'Missing fields', 'status': 400}
ACTIONS= {
    'unsubscribe': {
        'true': 'You will no longer receive emails from Hoard.',
        'false': 'You are still set to receive emails from Hoard.'
    }
}

logging_config = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console", "access_file_handler"],
            "propagate": True,
            "qualname": "sanic.access"
        }
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },
        "access_file_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": "/var/log/tmp/info.log",
            "formatter": "access"
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: " +
                      "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
    }
)

env = Environment(
    loader=PackageLoader('crypto_nlp', 'templates'),
    autoescape=select_autoescape(['html'])
)
unsub_temp = env.get_template('unsubscribe.html').render(url="/email_preferences")
not_found_temp = env.get_template('page_not_found.html')
login_temp = env.get_template('login.html').render(url="http://smaugdev.hoardinvest.com/login")
app = Sanic('test')

def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    return [dict(r.items()) for r in records]

@app.route('/unsubscribe/')
async def unsubscribe(request):
    print (request.path)
    print (request.cookies)
    return response.html(unsub_temp)

@app.route('/login')
async def unsubscribe(request):
    print (request.cookies)
    return response.html(login_temp)

@app.route('/email_preferences', methods=['PUT', 'GET'])
async def email_preferences(request):
    if request.method == 'PUT':
        if request.json.keys() != {'receive_emails_enabled'}:
            return error_response([MISSING_FIELDS])
        return response.json({'success':
            'Your email preferences have been updated'})

@app.route('/response', methods=['GET'])
async def result(request):
    args = request.args
    if len(args) > 2:
        return response.html(not_found_temp.render(), status=404)
    try:
        args_action = args['action'][0]
        args_result = args['success'][0]
        action = ACTIONS[args_action]
        result = action[args_result]
    except KeyError:
        return response.html(not_found_temp.render(), status=404)
    response_template = env.get_template('response.html').render(
        action=action, result=result)
    return response.html(response_template)


@app.route('/pop')
async def populate(request):
    await app.pg.execute('drop table if exists data')
    await app.pg.execute(""" create table data(
        id serial primary key,
        stuff text);
        """)
    for i in range(0, 1000):
        await app.pg.execute(f"insert into data (stuff) values ({i})")
    return response.HTTPResponse(body=None, status=200)


@app.route('/test_async')
async def index(request):
    """async with app.pool.acquire() as connection:
        results = await connection.fetch('SELECT * FROM data')
        connection.close()
        return response.HTTPResponse(body=None, status=200)
        #return json({'posts': jsonify(results)})"""



    results = await app.pg.fetch("select * from data")
    #print(result)
    return response.HTTPResponse(body=None, status=200)
    return response.json({'posts': jsonify(results)})


@app.route('/test_psy')
async def index(request):
    db = app.db_psy.cursor()
    db.execute("select * from data")
    result = db.fetchall()
    #print(result)
    return response.HTTPResponse(body=None, status=200)



"""@app.listener('before_server_start')
async def register_db(app, loop):
    app.pool = await create_pool(**app.db, loop=loop, max_size=100)
    async with app.pool.acquire() as connection:
        await connection.execute('DROP TABLE IF EXISTS data')
        await connection.execute(create table data(
            id serial primary key,
            stuff text);)
        for i in range(0, 1000):
            await connection.execute(f"insert into data (stuff) values ({i})")"""



@app.route('/posts/<post_id>')
async def post_handler(request, post_id):
    print (dir(request))
    print (request.args)
    return response.text('Post - {}'.format(post_id))


@app.route('/')
async def test(request):
    print (app.db)
    return response.text('Hello World!')

if __name__ == "__main__":

    app.blueprint(bp)
    app.db = dict(database="test_async",
                             user="arellok",
                             password="test",
                             host='127.0.0.1',
                             port=5432)

    app.db_psy = psycopg2.connect(dbname="test_async",
                         user="arellok",
                         password="test",
                         host='127.0.0.1',
                         port=5432)
    app.run(host='127.0.0.1', port=8000, access_log=False)
