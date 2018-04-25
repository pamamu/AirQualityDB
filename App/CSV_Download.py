import urllib


def df(url):

    csv = urllib.urlopen(url).read()  # returns type 'str'
    with open('datos.csv', 'w') as fx:  # str, hence mode 'w'
        fx.write(csv)


if __name__ == '__main__':
    df("http://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv")
