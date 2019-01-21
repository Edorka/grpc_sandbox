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
"""The Python implementation of the GRPC meterology.Greeter client."""

from __future__ import print_function
import logging

import grpc
import tqdm
from proto import meterology_pb2_grpc
from load import load, transform


class Transmision:

    def __init__(self, channel):
        self.channel = channel
        self.process = tqdm.tqdm()
        self.created = 0
        self.repeated = 0
        self.rejected = 0

    def report(self):
        status_tmpl = ('{0.created} items created, '
                       '{0.repeated} repeated, '
                       '{0.rejected} rejected.')
        self.process.update(1)
        self.process.set_description(status_tmpl.format(self))

    def send(self, item):
        try:
            stub = meterology_pb2_grpc.GreeterStub(self.channel)
            stub.GetPoI(item)
            self.created += 1
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                self.repeated += 1
            elif e.code() == grpc.StatusCode.FAILED_PRECONDITION:
                self.rejected += 1
            else:
                print('SendReading failed with {0}: {1}'.format(e.code(), e.details()))
                raise e
        finally:
            self.report()


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    source = transform(load('hourly_16.json'))
    with grpc.insecure_channel('localhost:50051') as channel:
        transmision = Transmision(channel)
        for meterology in source:
            transmision.send(meterology)


if __name__ == '__main__':
    logging.basicConfig()
    run()
