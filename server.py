import socket
import threading
from entities.grid import Grid
from entities.color_picker import ColorPicker
from datetime import datetime
last_request= {}

class SocketHandler:
    def __init__(self, host, port, receive_callback=None):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # List to store connected clients
        self.clients_lock = threading.Lock()  # Lock for synchronizing access to self.clients
        self.receive_callback = receive_callback
        self.grid =Grid((640, 480))
        self.grid.append_grid()
        self.color_picker = ColorPicker((200, 480), 640)

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                self.send_initialization_string(client_socket)
                with self.clients_lock:
                    self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()

    def send_initialization_string(self, client_socket):
        init_array = self.grid.get_checked_array()
        print(len(init_array))
        message = "init;" + str(init_array)
        client_socket.send(message.encode('utf-8'))

    def handle_client(self, client_socket):
        global last_request
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                #print(f"Received message from {client_socket.getpeername()}: {message}")
                peer_address = f"{client_socket.getpeername()[0]}.{client_socket.getpeername()[1]}"
                data = list(map(str, message.split(';')))

                if data[0] == 'click':
                    # if plays in board
                    if int(data[2]) < 32:
                        #no last request
                        if peer_address not in last_request:
                            last_request[peer_address] = data[5]
                            self.grid.check_by_grid_coordinate(int(data[2]),int(data[3]),int(data[1]),int(data[4]), self.color_picker.colors)
                            self.send_to_all_clients(message)
                        #if there is a last request
                        else:
                            last_call = datetime.strptime(last_request[peer_address], "%Y-%m-%d %H:%M:%S")
                            now = datetime.strptime(data[5], "%Y-%m-%d %H:%M:%S")
                            #check last request
                            if (now-last_call).total_seconds() >10:
                                last_request[peer_address] = data[5]
                                self.grid.check_by_grid_coordinate(int(data[2]),int(data[3]),int(data[1]),int(data[4]), self.color_picker.colors)
                                self.send_to_all_clients(message)
                            else:
                                client_message = "you have to wait " + str(10-int((now-last_call).total_seconds())) + " seconds"
                                print(client_message)
                                client_socket.send(client_message.encode('utf-8'))
                                
                    else:
                        self.grid.check_by_grid_coordinate(int(data[2]),int(data[3]),int(data[1]),int(data[4]), self.color_picker.colors)
                        self.send_to_all_clients(message)

        except socket.error:
            print(f"Connection with {client_socket.getpeername()} closed.")
        finally:
            with self.clients_lock:
                self.clients.remove(client_socket)
            client_socket.close()

    def send_to_all_clients(self, message):
        with self.clients_lock:
            for client in self.clients:
                try:
                    client.sendall(message.encode('utf-8'))
                except socket.error:
                    # Handle errors (e.g., disconnected clients)
                    pass

    def close(self):
        with self.clients_lock:
            for client_socket in self.clients:
                client_socket.close()

if __name__ == "__main__":
    server = SocketHandler('127.0.0.1', 2000)
    server.start_server()
