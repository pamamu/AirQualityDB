import rethinkdb as r
from itertools import islice


def connect_db(host, port):
    return r.connect(host, port).repl()


def close_db(conn):
    conn.close


def create_db(conn, db_name):
    r.db_create(db_name).run(conn)


def drop_db(conn, db_name):
    r.db_drop(db_name).run(conn)
    print ('Database {} dropped'.format(db_name))


def create_table(conn, db_name, table_name):
    r.db(db_name).table_create(table_name).run(conn)


def insert_data(conn, db_name, table_name, data):
    r.db(db_name).table(table_name).insert(data).run(conn)


def retrieve_data(conn, db_name, table_name):
    cursor = r.db(db_name).table(table_name).run(conn)
    for document in cursor:
        print document


def drop_table(conn, db_name, table_name):
    r.db(db_name).table_drop(table_name).run(conn)


def exist_db(conn,db_name):
    array = r.db_list().run(conn)
    return db_name in array


def create_geospatial_index(conn, db_name, table_name, index_name):
    r.db(db_name).table(table_name).index_create(index_name, geo=True).run(conn)


def nearest_points(conn, db_name, table_name, index_name, latitude, longitude, points=1):
    point = r.point(latitude, longitude)
    near = r.db(db_name).table(table_name).get_nearest(point, index=index_name, max_results=points, unit='m').run(conn)
    array = []
    for d in near:
        array.append(d)
    return array


def exist_index(conn, db_name, table_name, index_name):
    return index_name in r.db(db_name).table(table_name).index_list().run(conn)


def wait_index(conn, db_name, table_name, index_name):
    r.db(db_name).table(table_name).index_wait(index_name).run(conn)


def get_table(conn, db_name, table_name):
    data = r.db(db_name).table(table_name).run(conn)
    array = []
    for d in data:
        array.append(d)
    return array


def get_item(conn, db_name, table_name, id):
    data = r.db(db_name).table(table_name).get(id).run(conn)
    return data


def get_datos_estacion(conn, db_name, id):
    data = r.db(db_name).table("datos").eq_join("ESTACION", r.db("AirQuality").table("estaciones")).zip().filter({"ESTACION":id}).run(conn)
    array = []
    for d in data:
        array.append(d)
    return array


def get_datos_estacion_magnitud(conn, db_name, id_estacion, id_magnitud):
    data = r.db(db_name).table("datos").eq_join("ESTACION", r.db("AirQuality").table("estaciones")).zip().filter({"ESTACION":id_estacion}).filter({"MAGNITUD":id_magnitud}).run(conn)
    array = []
    for d in data:
        array.append(d)
    return array


if __name__ == '__main__':
    # Incluir esta consulta: r.db("AirQuality").table("datos").eqJoin("ESTACION", r.db("AirQuality").table("estaciones"))
    connection = connect_db("localhost", 28015)
    create_db(connection, 'test2')
    create_table(connection, 'test2', 'ejemplo')
    drop_table(connection, 'test2', 'ejemplo')
    drop_db(connection, 'test2')
    close_db(connection)
