from proto.meteorology_pb2 import Reading
from google.protobuf import json_format
import gzip
import json


def as_reading(item):
    try:
        result = Reading()
        return json_format.Parse(item, result, ignore_unknown_fields=False)

    except ValueError as error:
        print('not valid item', item, error, item)
        return []
    except json_format.ParseError as error:
        print('not valid item', error)
        print(json.dumps(json.loads(item), indent=4))
        raise error


def load(filepath):
    with gzip.open('hourly_16.json.gz', 'rt') as source:
        for line in source:
            yield line


if __name__ == '__main__':
    for reading_string in load('hourly_16.json.gz'):
        result = as_reading(reading_string)
        print(result)
