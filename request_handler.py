import os
from compression import gzip_compress
from utils import parse_headers, create_response


def handle_client(conn, addr, directory):
    try:
        with conn:
            reader = conn.makefile("rb")
            writer = conn.makefile("wb")

            request_line = reader.readline().decode().strip()
            method, req_path, _ = request_line.split(" ")

            print(f"Received request: {method} {req_path}")

            headers = parse_headers(reader)
            supports_gzip = "gzip" in headers.get("accept-encoding", "").lower().split(
                ","
            )

            if req_path.startswith("/files/"):
                handle_files(
                    method, req_path, headers, reader, writer, directory, supports_gzip
                )
            elif req_path == "/":
                handle_root(writer)
            elif req_path.startswith("/echo/"):
                handle_echo(req_path, writer, supports_gzip)
            elif req_path == "/user-agent":
                handle_user_agent(headers, writer, supports_gzip)
            else:
                handle_not_found(writer)

    except Exception as e:
        print(f"Error handling connection from {addr}: {e}")
    finally:
        print(f"Closing connection from {addr}")
        conn.close()


def handle_files(method, req_path, headers, reader, writer, directory, supports_gzip):
    filename = req_path[len("/files/") :]
    file_path = os.path.join(directory, filename)

    if method.upper() == "POST":
        content_length = int(headers.get("content-length", 0))
        body = reader.read(content_length)
        with open(file_path, "wb") as file:
            file.write(body)
        response = create_response("201 Created", "")
        writer.write(response.encode())
        writer.flush()
        print(f"File {filename} created successfully")

    elif method.upper() == "GET":
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                file_content = file.read()
            response = create_response(
                "200 OK", file_content, "application/octet-stream", supports_gzip
            )
            writer.write(response)
            writer.flush()
        else:
            handle_not_found(writer)


def handle_root(writer):
    response = create_response("200 OK", "")
    writer.write(response.encode())
    writer.flush()


def handle_echo(req_path, writer, supports_gzip):
    response_body = req_path[len("/echo/") :]
    response = create_response("200 OK", response_body, "text/plain", supports_gzip)
    writer.write(response)
    writer.flush()


def handle_user_agent(headers, writer, supports_gzip):
    user_agent = headers.get("user-agent", "Unknown")
    response = create_response("200 OK", user_agent, "text/plain", supports_gzip)
    writer.write(response)
    writer.flush()


def handle_not_found(writer):
    response = create_response("404 Not Found", "")
    writer.write(response.encode())
    writer.flush()
