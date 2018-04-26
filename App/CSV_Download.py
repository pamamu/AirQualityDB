import urllib
import os

def download_file(url, filename):

    csv = urllib.urlopen(url).read()  # returns type 'str'
    with open(filename, 'w') as fx:  # str, hence mode 'w'
        fx.write(csv)


def drop_file(filename):
    os.remove(filename)


if __name__ == '__main__':
    download_file("http://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv")

