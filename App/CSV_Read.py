import pandas
import re

def read_file(filename):
    # Cargamos el contenido del fichero CSV
    data = pandas.read_csv(filename, sep=';', header=0)

    # Eliminamos las columnas PROVINCIA, MUNICIPIO y PUNTO_MUESTREO
    data.drop(data.columns[[0, 1, 4]], axis=1, inplace=True)

    # columnas es la cabecera del CSV quitando las columnas PROVINCIA, MUNICIPIO y PUNTO_MUESTREO
    columnas = [x for x in data.columns.get_values().tolist()]

    # Creamos una expresion regular para comprobar las horas
    r_horas = re.compile("H..")

    # Creamos una expresion regular para comprobar los valores
    r_valores = re.compile("V..")

    # Filtramos las horas posibles de la cabecera
    horas = filter(r_horas.match, columnas)
    # Filtramos los valores posibles de la cabecera
    valores = filter(r_valores.match, columnas)

    # Esta es la primera fila (despues de la cabecera)
    primera_fila = (data[valores].iloc[0].tolist())

    # Seleccionamos aquellas horas y las etiquetas de los valores
    horas_no_validas = [x for i, x in enumerate(horas) if primera_fila[i] == 'N']
    valores_v_y_n= [x for i, x in enumerate(valores)]

    # Eliminamos las columnas de horas no validas y las columnas de valores no validas
    data = data.drop(horas_no_validas, 1).drop(valores_v_y_n,1)

    # Lo mostramos en forma de DataFrame
    #df = pandas.DataFrame(data)
    #print df.columns

    #TODO: Hay que seleccionar todas las estaciones y ponerles un unico identificador para que sean mas sencillas las busquedas
    # Agrupamos por Estacion y creamos un diccionario
    diccionario = data.groupby('ESTACION').apply(lambda dfg: dfg.to_dict(orient='list'))#.to_dict()
    print(diccionario)
    return diccionario


if __name__ == '__main__':
    read_file('datos.csv')
