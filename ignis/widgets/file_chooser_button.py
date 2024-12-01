import os
from gi.repository import Gtk, GObject  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.widgets.label import Label
from ignis.widgets.box import Box
from ignis.widgets.icon import Icon
from ignis.widgets.file_dialog import FileDialog
from ignis.utils import Utils


class FileChooserButton(Gtk.Button, BaseWidget):
    """
    Bases: :class:`Gtk.Button`

    A button that allows the user to select a file.

    .. code-block :: python

        Widget.FileChooserButton(
            dialog=Widget.FileDialog(
                initial_path=os.path.expanduser("~/.wallpaper"),
                filters=[
                    Widget.FileFilter(
                        mime_types=["image/jpeg", "image/png"],
                        default=True,
                        name="Images JPEG/PNG",
                    )
                ]
            ),
            label=Widget.Label(label='Select', ellipsize="end", max_width_chars=20)
        )
    """

    __gtype_name__ = "IgnisFileChooserButton"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        dialog: FileDialog,
        label: Label,
        **kwargs,
    ):
        Gtk.Button.__init__(self)
        BaseWidget.__init__(self, **kwargs)

        self._dialog = dialog
        self._label = label

        self.__file_icon = Icon(visible=False, style="padding-right: 7px;")

        self.child = Box(
            child=[
                self.__file_icon,
                self.label,
                Icon(icon_name="document-open-symbolic", style="padding-left: 10px;"),
            ],
        )
        self.dialog.connect("file-set", lambda x, file: self.__sync(file.get_path()))

        if self.dialog.initial_path:
            self.__sync(self.dialog.initial_path)

        self.connect(
            "clicked",
            lambda *args: self.dialog.open_dialog(),
        )

    @GObject.Property
    def dialog(self) -> FileDialog:
        """
        - required, read-only

        An instance of :class:`~ignis.widgets.Widget.FileDialog`.
        """
        return self._dialog

    @GObject.Property
    def label(self) -> Label:
        """
        - required, read-only

        An instance of :class:`~ignis.widgets.Widget.Label`.
        """
        return self._label

    def __sync(self, path: str) -> None:
        self.label.label = os.path.basename(path)
        try:
            self.__file_icon.icon_name = Utils.get_file_icon_name(path, symbolic=True)
            self.__file_icon.visible = True
        except FileNotFoundError:
            pass
