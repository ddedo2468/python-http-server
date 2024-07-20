from compression import gzip_compress


def parse_headers(reader):
    headers = {}
    while True:
        line = reader.readline().decode().strip()
        if not line:
            break
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return headers


def create_response(status, body, content_type="text/plain", compress=False):
    if isinstance(body, str):
        body = body.encode()

    if compress:
        body = gzip_compress(body)
        headers = [
            f"HTTP/1.1 {status}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body)}",
            "Content-Encoding: gzip",
            "\r\n",
        ]
    else:
        headers = [
            f"HTTP/1.1 {status}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body)}",
            "\r\n",
        ]

    return "\r\n".join(headers).encode() + body
