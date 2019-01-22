from proto.meteorology_pb2 import Reading, City, Coordinates
from google.protobuf import json_format


def to_object(item):
    try:
        result = Reading()
        return json_format.Parse(item, result, ignore_unknown_fields=True)
    except ValueError as error:
        print('not valid item', item, error, item)
        return []
    except AttributeError as error:
        print('not valid item', error)
        return []


def load(filepath, field='data'):
    with open(filepath) as source:
        for line in source:
            yield line


if __name__ == '__main__':
    for reading in load('hourly_16.json', field='data'):
        result = to_object(reading)
        print(result)

    # transform(load('hourly_16.json.gz', field='features'))
