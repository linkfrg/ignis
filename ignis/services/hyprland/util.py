import socket
from typing import Generator


def get_socket_resp(sock: socket.socket) -> str:
    resp = sock.recv(8192)

    while True:
        new_data = sock.recv(8192)
        if not new_data:
            break
        resp += new_data

    return resp.decode()


def listen_socket(sock: socket.socket) -> Generator[str, None, None]:
    buffer = b""
    while True:
        new_data = sock.recv(8192)
        if not new_data:
            break
        buffer += new_data
        while b"\n" in buffer:
            data, buffer = buffer.split(b"\n", 1)
            yield data.decode("utf-8")
