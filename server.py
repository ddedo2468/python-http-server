import socket
import threading
from request_handler import handle_client


class HTTPServer:
    def __init__(self, host, port, directory):
        self.host = host
        self.port = port
        self.directory = directory
        self.server_socket = None

    def start(self):
        self.server_socket = socket.create_server(
            (self.host, self.port), reuse_port=True
        )
        self.server_socket.listen()

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(
                target=handle_client, args=(conn, addr, self.directory)
            )
            client_thread.start()
