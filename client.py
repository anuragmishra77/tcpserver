import socket
import threading

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect(("127.0.0.1", 8080))

print("Connected to server")

username = input("Enter your username: ")

client_socket.sendall(username.encode())


def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                print("Server disconnected")
                break

            print("\n" + data.decode())
            print("You: ", end="")

        except ConnectionResetError:
            print("Server disconnected")
            break


receiver_thread = threading.Thread(
    target=receive_messages
)

receiver_thread.start()


while True:
    message = input("You: ")

    if message.lower() == "/quit":
        client_socket.close()
        break

    client_socket.sendall(message.encode())