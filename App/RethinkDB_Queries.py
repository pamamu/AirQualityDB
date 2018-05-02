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


def drop_table(repl, db_name, table_name):
    r.db(db_name).table_drop(table_name).run(repl)


def exist_db(repl,db_name):
    array = r.db_list().run(repl)
    return db_name in array


if __name__ == '__main__':
    connection = connect_db("localhost", 28015)
    create_db(connection, 'test2')
    create_table(connection, 'test2', 'ejemplo')
    drop_table(connection, 'test2', 'ejemplo')
    drop_db(connection,'test2')
    close_db(connection)
