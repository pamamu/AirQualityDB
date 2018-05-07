import urllib2
import os

def download_file(url, filename):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()

    content = page.read()

    with open(filename, 'w') as fx:  # str, hence mode 'w'
        fx.write(content)


def drop_file(filename):
    os.remove(filename)


if __name__ == '__main__':
    download_file("http://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv","datos.csv")

