import os
from gi.repository import GObject, Gio  # type: ignore
from ignis.gobject import IgnisGObject
from typing import Callable

FLAGS = {
    None: Gio.FileMonitorFlags.NONE,
    "none": Gio.FileMonitorFlags.NONE,
    "watch_mounts": Gio.FileMonitorFlags.WATCH_MOUNTS,
    "send_moved": Gio.FileMonitorFlags.SEND_MOVED,
    "watch_hard_links": Gio.FileMonitorFlags.WATCH_HARD_LINKS,
    "watch_moves": Gio.FileMonitorFlags.WATCH_MOVES,
}

EVENT = {
    Gio.FileMonitorEvent.CHANGED: "changed",
    Gio.FileMonitorEvent.CHANGES_DONE_HINT: "changes_done_hint",
    Gio.FileMonitorEvent.MOVED_OUT: "moved_out",
    Gio.FileMonitorEvent.DELETED: "deleted",
    Gio.FileMonitorEvent.CREATED: "created",
    Gio.FileMonitorEvent.ATTRIBUTE_CHANGED: "attribute_changed",
    Gio.FileMonitorEvent.PRE_UNMOUNT: "pre_unmount",
    Gio.FileMonitorEvent.UNMOUNTED: "unmounted",
    Gio.FileMonitorEvent.MOVED: "moved",
    Gio.FileMonitorEvent.RENAMED: "renamed",
    Gio.FileMonitorEvent.MOVED_IN: "moved_in",
}

file_monitors = []


class FileMonitor(IgnisGObject):
    """
    Monitor changes of the file or directory.

    Example usage:

    .. code-block::

        Utils.FileMonitor(
            path="path/to/something",
            recursive=False,
            callback=lambda path, event_type: print(path, event_type),
        )
    """

    def __init__(
        self,
        path: str,
        recursive: bool = False,
        flags: str | None = None,
        callback: Callable | None = None,
        prevent_gc: bool = True,
    ):
        super().__init__()
        self._file = Gio.File.new_for_path(path)
        self._monitor = self._file.monitor(FLAGS[flags], None)
        self._monitor.connect("changed", self.__on_change)

        self._path = path
        self._flags = flags
        self._callback = callback
        self._recursive = recursive
        self._prevent_gc = prevent_gc

        self._sub_monitors: list[Gio.FileMonitor] = []
        self._sub_paths: list[str] = []

        if recursive:
            for root, dirs, _files in os.walk(path):
                for d in dirs:
                    subdir_path = os.path.join(root, d)
                    self.__add_submonitor(subdir_path)

        if prevent_gc:
            file_monitors.append(self)

        self.connect(
            "changed", lambda *args: self._callback(*args) if self._callback else None
        )

    @GObject.Signal(arg_types=(str, str))
    def changed(self, *args):
        """
        - Signal

        Emitted when the file or directory changed.

        Args:
            path (``str``): The path to the changed file or directory.
            event_type (``str``): The event type. A list of all event types described in :attr:`callback`.
        """
        pass

    def __on_change(self, file_monitor, file, other_file, event_type) -> None:
        path = file.get_path()
        self.emit("changed", path, EVENT[event_type])

        if self.recursive and os.path.isdir(path):
            self.__add_submonitor(path)

    def __add_submonitor(self, path: str) -> None:
        if path in self._sub_paths:
            return

        sub_gfile = Gio.File.new_for_path(path)
        monitor = sub_gfile.monitor(FLAGS[self.flags], None)
        monitor.connect("changed", self.__on_change)
        self._sub_monitors.append(monitor)
        self._sub_paths.append(path)

    @GObject.Property
    def path(self) -> str:
        """
        - required, read-only

        The path to the file or directory to be monitored.
        """
        return self._path

    @GObject.Property
    def flags(self) -> str | None:
        """
        - optional, read-only

        What the monitor will watch for.

        Possible values:

        - none
        - watch_mounts
        - send_moved
        - watch_hard_links
        - watch_moves

        See :class:`Gio.FileMonitorFlags` for more info.

        Default: ``None``.
        """
        return self._flags

    @GObject.Property
    def callback(self) -> Callable | None:
        """
        - optional, read-write

        A function to call when the file or directory changes.
        It should take two arguments:
        1. The path to the changed file or directory
        2. The event type.

        Default: ``None``.

        Event types:

        - changed
        - changes_done_hint
        - moved_out
        - deleted
        - created
        - attribute_changed
        - pre_unmount
        - unmounted
        - moved
        - renamed
        - moved_in

        See :class:`Gio.FileMonitorEvent` for more info.

        """
        return self._callback

    @callback.setter
    def callback(self, value: Callable) -> None:
        self._callback = value

    @GObject.Property
    def recursive(self) -> bool:
        """
        - optional, read-only

        Whether monitoring is recursive (monitor all subdirectories and files).

        Default: ``False``.
        """
        return self._recursive

    @GObject.Property
    def prevent_gc(self) -> bool:
        """
        - optional, read-only

        Whether to prevent the garbage collector from collecting this file monitor.

        Default: ``True``.
        """
        return self._prevent_gc

    def cancel(self) -> None:
        """
        Cancel the monitoring process.
        """
        self._monitor.cancel()
