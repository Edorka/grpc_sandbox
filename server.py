from concurrent import futures
import time

import grpc

import meterology_pb2
import meterology_pb2_grpc


class Greeter(meterology_pb2_grpc.GreeterServicer):

    def InsertPoI(self, request, context):
        return meterology_pb2. InsertConfirmation(id=1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meterology_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
