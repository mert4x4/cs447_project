import socket
import threading
import random
import time

def client_handler(client_socket, address):
    print(f"Accepted connection from {address}")

    while True:
        random_number = random.randint(1, 100)
        message = f"Random Number: {random_number}"
        client_socket.sendall(message.encode('utf-8'))
        
        time.sleep(1)

def start_server():
    host = '127.0.0.1'
    port = 2000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=client_handler, args=(client_socket, address))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
