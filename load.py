from proto.meteorology_pb2 import Reading
from google.protobuf import json_format
import gzip


def as_reading(item):
    try:
        result = Reading()
        return json_format.Parse(item, result, ignore_unknown_fields=True)
    except ValueError as error:
        print('not valid item', item, error, item)
        return []
    except AttributeError as error:
        print('not valid item', error)
        return []


def load(filepath):
    with gzip.open('hourly_16.json.gz') as source:
        for line in source:
            yield as_reading(line), len(line)


if __name__ == '__main__':
    for reading_string in load('hourly_16.json.gz'):
        result = as_reading(reading_string)
        print(result)
