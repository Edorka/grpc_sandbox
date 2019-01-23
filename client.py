# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC meteorology.Greeter client."""

from __future__ import print_function
import logging

import grpc
import tqdm
from proto import meteorology_pb2_grpc
from load import load


class Transmision:

    def __init__(self, channel):
        self.channel = channel
        self.process = tqdm.tqdm()
        self.created = 0
        self.repeated = 0
        self.rejected = 0
        self.transferred = 0
        self.received = 0

    def add_received(self, size):
        self.received += size

    def report(self):
        status_tmpl = ('{0.created} items created, '
                       '{0.repeated} repeated, '
                       '{0.rejected} rejected.'
                       ' {0.transferred}'
                       ' of {0.received}')
        self.process.update(1)
        self.process.set_description(status_tmpl.format(self))

    @classmethod
    def handle_rpc_error(self, error):
        code = error.code()
        if code == grpc.StatusCode.ALREADY_EXISTS:
            self.repeated += 1
        elif code == grpc.StatusCode.FAILED_PRECONDITION:
            self.rejected += 1
        else:
            details = error.details()
            report = 'SendReading failed with {0}: {1}'
            raise Exception(report.format(code, details))

    def send(self, item):
        try:
            stub = meteorology_pb2_grpc.StationStub(self.channel)
            stub.Report(item)
            self.created += 1
            self.transferred += item.ByteSize()
        except grpc.RpcError as error:
            self.handle_rpc_error(error)
        finally:
            self.report()


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    source = load('hourly_16.json.gz')
    with grpc.insecure_channel('localhost:8000') as channel:
        transmision = Transmision(channel)
        for reading, original_size in source:
            transmision.add_received(original_size)
            transmision.send(reading)


if __name__ == '__main__':
    logging.basicConfig()
    run()
