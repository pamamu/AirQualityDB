from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, send, emit
from threading import Thread
import rethinkdb as r
from rethinkdb import RqlRuntimeError

app = Flask(__name__)
socketio = SocketIO(app)
global thread
thread = None

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='secret!',
    DB_HOST='localhost',
    DB_PORT=28015,
    DB_NAME='calidad_aire'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    conn = r.connect(app.config['DB_HOST'], app.config['DB_PORT'])
    try:
        r.db_create(app.config['DB_NAME']).run(conn)
        r.db(app.config['DB_NAME']).table_create('datos').run(conn)
        r.db(app.config['DB_NAME']).table('datos').index_create('timestamp').run(conn)
        print 'Database setup completed. Now run the app without --setup.'
    except RqlRuntimeError:
        print 'App database already exists. Run the app without --setup.'
    finally:
        conn.close()

@app.before_request
def before_request():
    try:
        g.db_conn = r.connect(host=app.config['DB_HOST'],
                              port=app.config['DB_PORT'],
                              db=app.config['DB_NAME'])
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.db_conn.close()
    except AttributeError:
        pass

@app.route('/', methods=['GET'])
def show_info():

    datos = list(r.db('calidad_aire').table('datos').order_by(index=r.desc('timestamp')).run(g.db_conn, time_format="raw"))
    print(datos)
    return render_template('index.html', datos=datos)

def cambios_datos():
    conn = r.connect(host=app.config['DB_HOST'],
                     port=app.config['DB_PORT'],
                     db=app.config['DB_NAME'])
    estaciones = r.table("datos").changes().run(conn)
    for chat in estaciones:
        chat['new_val']['estacion'] = str(chat['new_val']['estacion'])
        socketio.emit('nuevo_dato')


if __name__ == "__main__":
    # init_db()
    # Set up rethinkdb changefeeds before starting server
    if thread is None:
        thread = Thread(target=cambios_datos)
        thread.start()
    socketio.run(app, host='0.0.0.0', port=8081)
