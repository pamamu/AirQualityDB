import rethinkdb as r
import CSV_Download as d
import CSV_Read as csv


def connect_db(host, port):
    return r.connect(host, port).repl()


def close_db(repl):
    repl.close


def create_db(repl, db_name):
    r.db_create(db_name).run(repl)


def drop_db(repl, db_name):
    r.db_drop(db_name).run(repl)
    print ('Database {} dropped'.format(db_name))


def create_table(repl, db_name, table_name):
    r.db(db_name).table_create(table_name).run(repl)


def insert_data(repl, db_name, table_name, data):
    r.db(db_name).table(table_name).insert(data).run(repl)


def retrieve_data(repl, db_name, table_name):
    cursor = r.db(db_name).table(table_name).run(repl)
    for document in cursor:
        print document


if __name__ == '__main__':
    #TODO: Esto es una prueba. No tener en cuenta este fragmento de codigo
    connection = connect_db("localhost", 28015)
    filename = 'datos.csv'
    d.download_file("http://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv", filename)
    data = csv.read_file(filename)
    d.drop_file(filename)
    drop_db(connection, 'test2')
    create_db(connection, 'test2')
    create_table(connection, 'test2', 'ejemplo')
    insert_data(connection, 'test2', 'ejemplo', data)
    retrieve_data(connection, 'test2', 'ejemplo')
    close_db(connection)
