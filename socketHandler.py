import socket
import threading

class SocketHandler:
    def __init__(self, host, port, receive_callback=None):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_event = threading.Event()
        self.receive_callback = receive_callback

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_message(self, message):
        self.client_socket.sendall(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                self.client_socket.settimeout(5)
                data = self.client_socket.recv(20000)
                if data:
                    message = data.decode('utf-8')
                    #print(f"Received message: {message}")
                    if self.receive_callback:
                        self.receive_callback(message)  # Call the external callback function
                    self.receive_event.set()  # Trigger the receive event
            except socket.error:
                # No data received
                pass

    def start_receive_thread(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True  # Daemonize the thread, so it exits when the main thread exits
        receive_thread.start()

    def close(self):
        self.client_socket.close()
