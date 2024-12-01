import socket
from typing import Generator


def send_socket(sock: socket.socket, message: str) -> str:
    """
    Send a message to the socket.

    Args:
        sock: An instance of a socket.
        message: The message to send.

    Returns:
        The response from the socket.
    """
    sock.send(message.encode())
    resp = sock.recv(8192)

    while True:
        new_data = sock.recv(8192)
        if not new_data:
            break
        resp += new_data

    return resp.decode()


def listen_socket(sock: socket.socket) -> Generator[str, None, None]:
    """
    Listen to the socket.
    This function is a generator.

    Args:
        sock: An instance of a socket.

    Returns:
        A generator that yields responses from the socket.

    Example usage:

    .. code-block:: python

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect("path/to/socket.sock")

            for message in Utils.listen_socket(sock):
                print(message)
    """

    buffer = b""
    while True:
        new_data = sock.recv(8192)
        if not new_data:
            break
        buffer += new_data
        while b"\n" in buffer:
            data, buffer = buffer.split(b"\n", 1)
            yield data.decode("utf-8")
