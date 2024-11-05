from __future__ import annotations
import os
from gi.repository import Gtk, GObject, Gio, GLib  # type: ignore
from typing import Callable
from ignis.widgets.file_filter import FileFilter
from ignis.gobject import IgnisGObject


class FileDialog(Gtk.FileDialog, IgnisGObject):
    """
    Bases: `Gtk.FileDialog <https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/FileDialog.html>`_.

    .. danger::
        This is not a regular widget.
        It doesn't support common widget properties and cannot be added as a child to a container.

    A window that allows the user to select a file.

    Signals:
        - file-set (``Gio.File``): Emitted when a file or folder is selected.

    .. code-block :: python

        Widget.FileDialog(
            initial_path=os.path.expanduser("~/.config"),
            on_file_set=lambda self, file: print(file.get_path()),
            select_folder=False,
            filters=[
                Widget.FileFilter(
                    mime_types=["image/jpeg", "image/png"],
                    default=True,
                    name="Images JPEG/PNG",
                )
            ]
        )
    """

    __gtype_name__ = "IgnisFileDialog"
    __gsignals__ = {
        "file-set": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (Gio.File,)),
    }

    def __init__(self, **kwargs):
        Gtk.FileDialog.__init__(self)
        self._file: Gio.File | None = None
        self._list_store = Gio.ListStore.new(Gtk.FileFilter)

        self._filters: list[FileFilter] = []
        self._on_file_set: Callable | None = None
        self._initial_path: str | None = None
        self._select_folder: bool = False
        IgnisGObject.__init__(self, **kwargs)

        self.connect(
            "file-set",
            lambda x, file: self.on_file_set(x, file) if self.on_file_set else None,
        )

    def open_dialog(self) -> None:
        """
        Open dialog.
        """
        if self.select_folder:
            super().select_folder(Gtk.Window(), None, self.__open_callback)
        else:
            super().open(Gtk.Window(), None, self.__open_callback)

    def __open_callback(self, dialog, result) -> None:
        try:
            if self.select_folder:
                file = self.select_folder_finish(result)
            else:
                file = dialog.open_finish(result)
        except GLib.GError:  # type: ignore
            return

        if file is not None:
            self._file = file
            self.emit("file-set", file)
            self.notify("file")

    @GObject.Property
    def file(self) -> Gio.File | None:
        """
        - not argument, read-only

        The selected ``Gio.File``.

        .. hint::
            Use the ``get_path`` method on the ``Gio.File`` to get the path.
        """
        return self._file

    @GObject.Property
    def on_file_set(self) -> Callable:
        """
        - optional, read-write

        A function to call when user selects a file.
        """
        return self._on_file_set

    @on_file_set.setter
    def on_file_set(self, value: Callable) -> None:
        self._on_file_set = value

    @GObject.Property
    def filters(self) -> list[FileFilter]:
        """
        - optional, read-write

        A list of file filters.
        """
        return self._filters

    @filters.setter
    def filters(self, value: list[FileFilter]) -> None:
        self._list_store.remove_all()
        super().set_filters(self._list_store)
        for i in value:
            self.add_filter(i)

    @GObject.Property
    def initial_path(self) -> str:
        """
        - optional, read-write

        The path to the folder or file that will be selected by default.
        """
        return self._initial_path

    @initial_path.setter
    def initial_path(self, value: str) -> None:
        self._initial_path = value
        gfile = Gio.File.new_for_path(value)
        if os.path.isdir(value):
            self.set_initial_folder(gfile)
        elif os.path.isfile(value):
            self.set_initial_file(gfile)

    @GObject.Property
    def select_folder(self) -> bool:
        """
        - optional, read-write

        Whether the dialog should allow selecting folders instead of files.
        """
        return self._select_folder

    @select_folder.setter
    def select_folder(self, value: bool) -> None:
        self._select_folder = value

    def add_filter(self, filter: FileFilter) -> None:
        """
        Add a filter.

        Args:
            filter (:class:`~ignis.widgets.FileFilter`): The instance of filter to add.
        """
        self._list_store.append(filter)

        super().set_filters(self._list_store)
        if filter.default:
            self.set_default_filter(filter)

        self._filters.append(filter)
