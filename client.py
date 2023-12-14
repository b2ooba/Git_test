import threading
import time
import socket

class client:
    def __init__(self, server_ip = "127.0.0.1", port=8999):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server(server_ip, port)
        def connect_to_server(self, ip, port):
            try:
                print("Connecting to the Server...")
                self.server_socket.connect((ip,port))
                print("Connected.")
            except Exception as e:
                print("Error Connecting to the Server : ", str(e))
