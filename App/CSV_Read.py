import pandas
import re
import json


class CSVRead:
    def __init__(self, filename):
        data = pandas.read_csv(filename, sep=';', header=0)
        data.drop(data.columns[[0, 1, 4]], axis=1, inplace=True)
        columnas = [x for x in data.columns.get_values().tolist()]
        r = re.compile("H..")
        raux = re.compile("V..")
        horas = filter(r.match, columnas)
        horas_validas = filter(raux.match, columnas)
        valores_horas_validas = (data[horas_validas].iloc[0].tolist())
        # print(valores_horas_validas)
        horas_sensor = [x for i, x in enumerate(horas) if valores_horas_validas[i] == 'V']
        # print(horas_sensor)
        diccionario = data.groupby('ESTACION').apply(lambda dfg: dfg.drop('ESTACION', axis=1).to_dict(orient='list')).to_dict()
        # diccionario = json.dumps(diccionario)
        print(diccionario)



if __name__ == '__main__':
    CSVRead('convertcsv.csv')