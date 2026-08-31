import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 8080))

server.listen(5)

print("HTTP server running on http://localhost:8080")


while True:

    client_socket, client_address = server.accept()

    print("\nClient connected:", client_address)

    # Receive HTTP request
    request = client_socket.recv(4096)

    request_text = request.decode()

    # Get first line
    request_line = request_text.split("\r\n")[0]

    # Split request line
    parts = request_line.split(" ")

    method = parts[0]
    path = parts[1]
    version = parts[2]

    print("Method:", method)
    print("Path:", path)
    print("Version:", version)

    # Routing

    if path == "/":

        with open("index.html", "r") as file:
            body = file.read()

        status = "200 OK"
        content_type = "text/html"

    elif path == "/about":

        body = "About Page"
        status = "200 OK"
        content_type = "text/plain"

    elif path == "/contact":

        body = "Contact Page"
        status = "200 OK"
        content_type = "text/plain"

    else:

        body = "Page Not Found"
        status = "404 Not Found"
        content_type = "text/plain"

    # Convert body to bytes

    body_bytes = body.encode()

    # Create HTTP response

    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
    ).encode() + body_bytes

    # Send response

    client_socket.send(response)

    # Close connection

    client_socket.close()