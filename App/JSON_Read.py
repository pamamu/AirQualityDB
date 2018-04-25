import simplejson as js
import re
import time
import datetime


def del_coments(data, ch="#"):
    salida = ""
    for line in data.splitlines():
        if line.find(ch) > -1:
            line = line[0:line.find(ch)]
        salida = salida + line + "\n"
    return salida


def get_field(data, field, enable=True):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []
    if field == 'date':
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%d%B%y_%H-%M-%S')
        fields_found.append(st)
        return fields_found

    for key, value in data.iteritems():
        if key == field:
            if isinstance(value, list):
                fields_found = fields_found + value
            else:
                fields_found.append(value)
        elif isinstance(value, dict):
            results = get_field(value, field)
            for result in results:
                fields_found.append(result)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_field(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)
    return fields_found


def substitute_params(data, prejson, reg="<.*?>"):
    while len(re.findall(reg, data)) > 0:
        for match in re.findall(reg, data):
            m = match.replace('<', '').replace('>', '')
            data = data.replace(match, get_field(prejson, m)[0])
    return data


class JsonRead(object):
    def __init__(self, filename):
        self.json = self.load_json(filename)

    def load_json(self, filename):
        if filename.find(".json") < 0:
            filename = filename + ".json"
        try:
            data = open(filename).read()
            data = del_coments(data)
            prejson = js.loads(data)
            data = substitute_params(data, prejson)
        except:
            print("ERROR: loading %s" % (filename))
            raise
        return js.loads(data)


if __name__ == "__main__":
    reader = JsonRead("configuration.json")
    print (reader.json)
