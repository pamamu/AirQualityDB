from flask import Flask
from flask import json
import RethinkDB_Queries as q
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Bienvenido a la API de AirQuality'


@app.route('/estacion')
def estaciones():
    connection = q.connect_db('localhost', 28015)
    data = q.get_table(connection, 'AirQuality', 'estaciones')
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response

@app.route('/estacion/<int:estacion>')
def estacion_id(estacion):
    connection = q.connect_db('localhost', 28015)
    data = q.get_item(connection, 'AirQuality', 'estaciones', estacion)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response


@app.route('/magnitud')
def magnitudes():
    connection = q.connect_db('localhost', 28015)
    data = q.get_table(connection, 'AirQuality', 'magnitudes')
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response

@app.route('/magnitud/<int:magnitud>')
def magnitud_id(magnitud):
    connection = q.connect_db('localhost', 28015)
    data = q.get_item(connection, 'AirQuality', 'magnitudes', magnitud)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response


@app.route('/dato')
def datos():
    connection = q.connect_db('localhost', 28015)
    data = q.get_table(connection, 'AirQuality', 'datos')
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response

@app.route('/dato/<string:dato>')
def dato_id(dato):
    connection = q.connect_db('localhost', 28015)
    data = q.get_item(connection, 'AirQuality', 'datos', dato)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response


@app.route('/datos/<int:estacion>')
def datos_estacion(estacion):
    connection = q.connect_db('localhost', 28015)
    data = q.get_datos_estacion(connection, 'AirQuality', estacion)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response


@app.route('/datos/<int:estacion>/<int:magnitud>')
def datos_estacion_magnitud(estacion, magnitud):
    connection = q.connect_db('localhost', 28015)
    data = q.get_datos_estacion_magnitud(connection, 'AirQuality', estacion, magnitud)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    q.close_db(connection)
    return response


if __name__ == '__main__':
    app.run()

