import RethinkDB_Queries as r
import CSV_Download as d
import CSV_Read as csv

# Conexion a la base de datos
connection = r.connect_db("localhost", 28015)

# Nombre del fichero
filename_data = 'datos.csv'
filename_magnitudes = 'mag.csv'
filename_estaciones = 'stations.csv'

# Nombre de la base de datos
db_name = 'AirQuality'
table_data = 'datos'
table_mag = 'magnitudes'
table_sta = 'estaciones'

# Descarga del fichero
#d.download_file("http://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv", filename)

# Procesado del fichero de datos en 'data', de magnitudes en 'magnitudes' y de estaciones en 'estaciones'
data = csv.read_file_data(filename_data)
#magnitudes = csv.read_file_magnitudes(filename_magnitudes)
#estaciones = csv.read_file_estaciones(filename_estaciones)

# Una vez procesado, borramos el fichero
#d.drop_file(filename)

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

# Mostramos los datos desde la BD
r.retrieve_data(connection, db_name, table_data)

# Cerramos la conexion
r.close_db(connection)

