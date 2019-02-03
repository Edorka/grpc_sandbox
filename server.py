from concurrent import futures
import time

import grpc

from proto import meteorology_pb2, meteorology_pb2_grpc


class Greeter(meteorology_pb2_grpc.StationServicer):

    def Report(self, request, context):
        return meteorology_pb2.ConfirmationMessage(value='done')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meteorology_pb2_grpc.add_StationServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
