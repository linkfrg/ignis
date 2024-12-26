from ignis.widgets import Widget
from .util import get_wifi_connect_window_name


class WifiConnectDialog(Widget.RegularWindow):
    """
    :meta private:
    """

    def __init__(self, access_point) -> None:
        self._password_entry = Widget.Entry(
            visibility=False, hexpand=True, on_accept=lambda x: self.__connect_to()
        )
        self._access_point = access_point
        super().__init__(
            resizable=False,
            width_request=400,
            height_request=200,
            namespace=get_wifi_connect_window_name(access_point.bssid),
            style="padding: 1rem;",
            child=Widget.Box(
                vertical=True,
                child=[
                    Widget.Box(
                        child=[
                            Widget.Icon(
                                icon_name="dialog-password",
                                pixel_size=48,
                                style="margin-bottom: 2rem; margin-right: 2rem; margin-left: 1rem; margin-top: 1rem;",
                            ),
                            Widget.Box(
                                vertical=True,
                                spacing=20,
                                child=[
                                    Widget.Label(
                                        label="Authentication required by Wi-Fi network",
                                        style="font-size: 1.1rem;",
                                    ),
                                    Widget.Label(
                                        label=f'Passwords or encryption keys are required to access the Wi-Fi network "{access_point.ssid}".',
                                        wrap=True,
                                        max_width_chars=30,
                                        style="font-weight: normal;",
                                    ),
                                ],
                            ),
                        ]
                    ),
                    Widget.Box(
                        child=[Widget.Label(label="Password"), self._password_entry],
                        spacing=10,
                        style="margin-top: 1rem;",
                    ),
                    Widget.CheckButton(
                        label="Show password",
                        active=True,
                        on_toggled=lambda x,
                        active: self._password_entry.set_visibility(not active),
                        style="margin-left: 5.5rem; margin-top: 0.5rem;",
                    ),
                    Widget.Box(
                        vexpand=True,
                        valign="end",
                        halign="end",
                        spacing=10,
                        child=[
                            Widget.Button(
                                label="Cancel",
                                on_click=lambda x: self.unrealize(),
                            ),
                            Widget.Button(
                                sensitive=self._password_entry.bind(
                                    "text", lambda value: len(value) >= 8
                                ),
                                label="Connect",
                                on_click=lambda x: self.__connect_to(),
                            ),
                        ],
                    ),
                ],
            ),
        )

    def __connect_to(self) -> None:
        if len(self._password_entry.text) >= 8:
            self._access_point.connect_to(self._password_entry.text)
            self.unrealize()
