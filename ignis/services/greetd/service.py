import os
import socket
import json
from gi.repository import GObject  # type: ignore
from ignis.base_service import BaseService
from ignis.exceptions import GreetdSockNotFoundError
from .response import (
    GreetdSuccessResponse,
    GreetdErrorResponse,
    GreetdAuthMessage,
    GreetdBaseResponse,
)

GREETD_SOCK = os.getenv("GREETD_SOCK", "")

GREETD_RESPONSES: dict[str, GreetdBaseResponse] = {
    "success": GreetdSuccessResponse,
    "error": GreetdErrorResponse,
    "auth_message": GreetdAuthMessage,
}

GreetdResponse = GreetdSuccessResponse | GreetdErrorResponse | GreetdAuthMessage


class GreetdService(BaseService):
    def __init__(self):
        super().__init__()
        self._sock: socket.socket | None = None

    @GObject.Property
    def is_available(self) -> bool:
        return os.path.exists(GREETD_SOCK)

    def __send_request(self, request: dict) -> str:
        if not self.is_available:
            raise GreetdSockNotFoundError()

        if not self._sock:
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._sock.connect(GREETD_SOCK)

        json_request = json.dumps(request)
        self._sock.send(
            len(json_request).to_bytes(4, "little") + json_request.encode("utf-8")
        )
        resp_raw = self._sock.recv(128)
        resp_len = int.from_bytes(resp_raw[0:4], "little")
        resp_trimmed = resp_raw[4 : resp_len + 4].decode()

        response = json.loads(resp_trimmed)

        return GREETD_RESPONSES[response["type"]](response)

    def create_session(self, username: str) -> GreetdResponse:
        return self.__send_request(
            request={"type": "create_session", "username": username}
        )

    def post_auth_message_response(self, response: str | None = None) -> GreetdResponse:
        request = {"type": "post_auth_message_response"}

        if response is not None:
            request["response"] = response

        return self.__send_request(request=request)

    def start_session(self, cmd: list[str], env: list[str]) -> GreetdResponse:
        return self.__send_request(
            request={"type": "start_session", "cmd": cmd, "env": env}
        )

    def cancel_session(self, username: str) -> GreetdResponse:
        return self.__send_request(request={"type": "cancel_session"})
