import datetime
from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.app import IgnisApp
from ignis.services.audio import AudioService
from ignis.services.system_tray import SystemTrayService, SystemTrayItem
from ignis.services.niri import NiriService
from ignis.services.notifications import NotificationService
from ignis.services.mpris import MprisService, MprisPlayer

app = IgnisApp.get_default()

app.apply_css(f"{Utils.get_current_dir()}/style.scss")


audio = AudioService.get_default()
system_tray = SystemTrayService.get_default()
niri = NiriService.get_default()
notifications = NotificationService.get_default()
mpris = MprisService.get_default()


def workspace_button(workspace: dict) -> Widget.Button:
    widget = Widget.Button(
        css_classes=["workspace"],
        on_click=lambda x, id=workspace["idx"]: niri.switch_to_workspace(id),
        child=Widget.Label(label=str(workspace["idx"])),
    )
    if workspace["is_active"] == True:
        widget.add_css_class("active")

    return widget


def scroll_workspaces(monitor_name: str, direction: str) -> None:
    current = list(filter(lambda w: w['is_active'] == True and w['output'] == monitor_name, niri.workspaces))[0]["idx"]
    if direction == "up":
        target = current + 1
        niri.switch_to_workspace(target)
    else:
        target = current - 1
        if target == 11:
            return
        niri.switch_to_workspace(target)


def workspaces(monitor_name: str) -> Widget.EventBox:
    return Widget.EventBox(
        on_scroll_up=lambda x: scroll_workspaces(monitor_name,"up"),
        on_scroll_down=lambda x: scroll_workspaces(monitor_name,"down"),
        css_classes=["workspaces"],
        spacing=5,
        child=niri.bind(
            "workspaces",
            transform=lambda value: [workspace_button(i) for i in value if i['output'] == monitor_name],
        ),
    )


def mpris_title(player: MprisPlayer) -> Widget.Box:
    return Widget.Box(
        spacing=10,
        setup=lambda self: player.connect(
            "closed",
            lambda x: self.unparent(),  # remove widget when player is closed
        ),
        child=[
            Widget.Icon(image="audio-x-generic-symbolic"),
            Widget.Label(
                ellipsize="end",
                max_width_chars=30,
                label=player.bind("title"),
            ),
        ],
    )


def media() -> Widget.Box:
    return Widget.Box(
        spacing=10,
        child=[
            Widget.Label(
                label="No media players",
                visible=mpris.bind("players", lambda value: len(value) == 0),
            )
        ],
        setup=lambda self: mpris.connect(
            "player-added", lambda x, player: self.append(mpris_title(player))
        ),
    )


def client_title(monitor_name) -> Widget.Label:
    return Widget.Label(
        ellipsize="end",
        max_width_chars=40,
        visible=niri.bind("active_output", lambda x: x["name"] == monitor_name),
        label=niri.bind(
            "active_window",
            transform=lambda value: "" if value is None else value["title"]
        ),
    )


def current_notification() -> Widget.Label:
    return Widget.Label(
        ellipsize="end",
        max_width_chars=20,
        label=notifications.bind(
            "notifications", lambda value: value[0].summary if len(value) > 0 else None
        ),
    )


def clock() -> Widget.Label:
    # poll for current time every second
    return Widget.Label(
        css_classes=["clock"],
        label=Utils.Poll(
            1_000, lambda self: datetime.datetime.now().strftime("%H:%M")
        ).bind("output"),
    )


def speaker_volume() -> Widget.Box:
    return Widget.Box(
        child=[
            Widget.Icon(
                image=audio.speaker.bind("icon_name"), style="margin-right: 5px;"
            ),
            Widget.Label(
                label=audio.speaker.bind("volume", transform=lambda value: str(value))
            ),
        ]
    )

def keyboard_layout() -> Widget.EventBox:
    return Widget.EventBox(
        on_click=lambda self: niri.switch_kb_layout(),
        child=[
            Widget.Label(
                label=niri.bind("kb_layout")
            )
        ]
    )
        

def tray_item(item: SystemTrayItem) -> Widget.Button:
    if item.menu:
        menu = item.menu.copy()
    else:
        menu = None

    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Icon(image=item.bind("icon"), pixel_size=24),
                menu,
            ]
        ),
        setup=lambda self: item.connect("removed", lambda x: self.unparent()),
        tooltip_text=item.bind("tooltip"),
        on_click=lambda x: menu.popup() if menu else None,
        on_right_click=lambda x: menu.popup() if menu else None,
        css_classes=["tray-item"],
    )


def tray():
    return Widget.Box(
        setup=lambda self: system_tray.connect(
            "added", lambda x, item: self.append(tray_item(item))
        ),
        spacing=10,
    )


def speaker_slider() -> Widget.Scale:
    return Widget.Scale(
        min=0,
        max=100,
        step=1,
        value=audio.speaker.bind("volume"),
        on_change=lambda x: audio.speaker.set_volume(x.value),
        css_classes=["volume-slider"],  # we will customize style in style.css
    )


def left(monitor_name: str) -> Widget.Box:
    return Widget.Box(child=[workspaces(monitor_name), client_title(monitor_name)], spacing=10)


def center() -> Widget.Box:
    return Widget.Box(
        child=[
            current_notification(),
            Widget.Separator(vertical=True, css_classes=["middle-separator"]),
            media(),
        ],
        spacing=10,
    )


def right() -> Widget.Box:
    return Widget.Box(
        child=[tray(), keyboard_layout(), speaker_volume(), speaker_slider(), clock()], spacing=10
    )


def bar(monitor_id: int = 0) -> Widget.Window:
    monitor_name=Utils.get_monitor(monitor_id).get_connector()
    return Widget.Window(
        namespace=f"ignis_bar_{monitor_id}",
        monitor=monitor_id,
        anchor=["left", "top", "right"],
        exclusivity="exclusive",
        child=Widget.CenterBox(
            css_classes=["bar"],
            start_widget=left(monitor_name),
            center_widget=center(),
            end_widget=right(),
        ),
    )


# this will display bar on all monitors
for i in range(Utils.get_n_monitors()):
    bar(i)
