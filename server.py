import socket
import threading

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind(("127.0.0.1", 8080))
server_socket.listen()

print("Server is listening on 127.0.0.1:8080")

clients = {}


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.sendall(message)


def handle_client(connection, address):
    print("Client connected:", address)

    try:
        username = connection.recv(1024).decode()

        clients[connection] = username

        print(username, "joined the chat")

        broadcast(
            f"{username} joined the chat".encode(),
            connection
        )

        while True:
            data = connection.recv(1024)

            if not data:
                break

            message = data.decode()

            print(username + ":", message)

            full_message = f"{username}: {message}"

            broadcast(
                full_message.encode(),
                connection
            )

    except ConnectionResetError:
        pass

    finally:
        username = clients.pop(connection, "Unknown")

        print(username, "disconnected")

        broadcast(
            f"{username} left the chat".encode(),
            connection
        )

        connection.close()


while True:
    connection, address = server_socket.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(connection, address)
    )

    client_thread.start()