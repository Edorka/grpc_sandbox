import json
from proto.meteorology_pb2 import Reading, City, Coordinates
from google.protobuf import json_format
import itertools


def to_object(item):
    
    try:
        return json_format.Parse(item, Reading, ignore_unknown_fields=True)
    except ValueError as error:
        print('not valid item', item, error)
        return []


def load(filepath, field='data'):
    with open(filepath) as source:
        for line in source:
            yield line


def transform(items):
    for item in items:
        yield poi_from_geojson(item)


if __name__ == '__main__':
    fields = Reading.DESCRIPTOR.fields
    for reading in load('hourly_16.json', field='data'):
        print(to_object(reading))

    # transform(load('hourly_16.json.gz', field='features'))
