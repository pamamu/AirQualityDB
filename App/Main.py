import RethinkDB_Queries as r
import CSV_Download as d
import CSV_Read as csv

import rethinkdb as rdb

from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, send, emit
from threading import Thread
from rethinkdb import RqlRuntimeError, RqlDriverError

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
    DB_NAME='AirQuality'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def db_work():
    # Conexion a la base de datos
    connection = r.connect_db("localhost", 28015)

    # Nombre del fichero
    filename_data = 'data.csv'
    filename_magnitudes = 'mag.csv'
    filename_estaciones = 'stations.csv'

    # Nombre de la base de datos
    db_name = 'AirQuality'
    table_data = 'datos'
    table_mag = 'magnitudes'
    table_sta = 'estaciones'

    # Descarga del fichero
    d.download_file("http://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv", filename_data)

    # Procesado del fichero de datos en 'data', de magnitudes en 'magnitudes' y de estaciones en 'estaciones'
    data = csv.read_file_data(filename_data)
    magnitudes = csv.read_file_magnitudes(filename_magnitudes)
    estaciones = csv.read_file_estaciones(filename_estaciones)

    # Una vez procesado, borramos el fichero
    d.drop_file(filename_data)

    # Si existe la base de datos la borramos
    if r.exist_db(connection, db_name):
        r.drop_db(connection, db_name)

    # Creamos la base de datos AirQuality, que contendra las tablas con
    # los datos, las estaciones y las magnitudes
    r.create_db(connection, db_name)
    r.create_table(connection, db_name, table_data)
    r.create_table(connection, db_name, table_sta)
    r.create_table(connection, db_name, table_mag)

    # Insertamos los datos obtenidos del CSV descargado
    r.insert_data(connection, db_name, table_data, data)
    r.insert_data(connection, db_name, table_mag, magnitudes)
    r.insert_data(connection, db_name, table_sta, estaciones)

    # Mostramos los datos desde la BD
    # r.retrieve_data(connection, db_name, table_data)
    # r.retrieve_data(connection, db_name, table_mag)
    # r.retrieve_data(connection, db_name, table_sta)

    # Creamos un indice geoespacial
    r.create_geospatial_index(connection, db_name, table_sta, 'coordenadas')
    r.wait_index(connection, db_name, table_sta, 'coordenadas')

    # Consultamos el punto mas cercano
    # r.nearest_points(connection, db_name, table_sta, 'coordenadas', 40.465156, -3.584270)

    # Cerramos la conexion
    r.close_db(connection)


@app.before_request
def before_request():
    g.db_conn = rdb.connect(host=app.config['DB_HOST'],
                            port=app.config['DB_PORT'],
                            db=app.config['DB_NAME'])


@app.teardown_request
def teardown_request(exception):
    try:
        g.db_conn.close()
    except AttributeError:
        pass


@app.route('/', methods=['GET'])
def show_info():
    estaciones = rdb.db(app.config['DB_NAME']).table('estaciones').run(g.db_conn)
    # for estacion in estaciones:
    #     print(estacion['coordenadas']['coordinates'])
    magnitudes = None

    estaciones_array = []
    for estacion in estaciones:
        datos_estacion = rdb.db('AirQuality').table('datos').eq_join("ESTACION",
                                                    rdb.db("AirQuality").table("estaciones")).zip().filter(
            {"ESTACION": estacion['id']}).eq_join("MAGNITUD", rdb.db("AirQuality").table('magnitudes')).zip().run(g.db_conn)

        estacion['datos'] = []
        for dato_estacion in datos_estacion:
            estacion['datos'].append(dato_estacion)

        # print(estacion)
        estaciones_array.append(estacion)
    datos = list(
        rdb.db('calidad_aire').table('datos').order_by(index=rdb.desc('timestamp')).run(g.db_conn, time_format="raw"))
    # print(datos)
    return render_template('index.html', datos=datos, estaciones=estaciones_array, magnitudes=magnitudes)


def cambios_datos():
    conn = rdb.connect(host=app.config['DB_HOST'],
                       port=app.config['DB_PORT'],
                       db=app.config['DB_NAME'])
    estaciones = rdb.table("datos").changes().run(conn)
    # for chat in estaciones:
    #     chat['new_val']['estacion'] = str(chat['new_val']['estacion'])
    #     socketio.emit('nuevo_dato')


if __name__ == '__main__':
    db_work()
    if thread is None:
        thread = Thread(target=cambios_datos)
        thread.start()
    socketio.run(app, host='0.0.0.0', port=8083)
