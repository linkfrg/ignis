from typing import Literal


class GreetdBaseResponse:
    def __init__(self, resp: dict[str, str], type_: str):
        self._resp = resp
        if resp["type"] != type_:
            raise ValueError(
                f"Incorrect response type: expected {type_}, got {resp['type']}"
            )

    @property
    def resp(self) -> dict[str, str]:
        return self._resp

    @property
    def resp_type(self) -> str:
        return self._resp["type"]


class GreetdSuccessResponse(GreetdBaseResponse):
    def __init__(self, resp: dict[str, str]):
        super().__init__(resp, "success")


class GreetdErrorResponse(GreetdBaseResponse):
    def __init__(self, resp: dict[str, str]):
        super().__init__(resp, "error")

    @property
    def error_type(self) -> Literal["auth_error", "error"]:
        return self._resp["error_type"]

    @property
    def description(self) -> str:
        return self._resp["description"]


class GreetdAuthMessage(GreetdBaseResponse):
    def __init__(self, resp: dict[str, str]):
        super().__init__(resp, "auth_message")

    @property
    def auth_message_type(self) -> Literal["visible", "secret", "info", "error"]:
        return self._resp["auth_message_type"]

    @property
    def auth_message(self) -> str:
        return self._resp["auth_message"]
