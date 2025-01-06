import sys
from ignis import CACHE_DIR
from gi.repository import GLib  # type: ignore
from ignis.options_manager import OptionsManager, OptionsGroup


def get_recorder_default_file_location() -> str | None:
    if "sphinx" not in sys.modules:
        return GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_VIDEOS)
    else:
        return "XDG Videos directory"


class Options(OptionsManager):
    """
    Options for Ignis.

    .. warning::

        Use already initialized instance of this class:

        .. code-block:: python

            from ignis.options import options

            print(options.notifications.dnd)

    Below are classes with options, their names begin with a capital letter.
    However, if you want to get the current value of an option or set a value,
    use an initialized instance that starts with a lowercase letter.

    For example:
        * ``Notifications`` -> ``notifications``
        * ``Recorder`` -> ``recorder``
        * and etc.

    You can use classes (not instances of them) to obtain default values of options.
    """

    def __init__(self):
        super().__init__(file=f"{CACHE_DIR}/ignis_options.json")

    class Notifications(OptionsGroup):
        """
        Options for the :class:`~ignis.services.notifications.NotificationService`.
        """

        #: Do Not Disturb mode.
        #:
        #: If set to ``True``, the ``new_popup`` signal will not be emitted,
        #: and all new :class:`~ignis.services.notifications.Notification` instances will have ``popup`` set to ``False``.
        dnd: bool = False

        #: The timeout before a popup is automatically dismissed, in milliseconds.
        popup_timeout: int = 5000

        #: The maximum number of popups.
        #:
        #: If the length of the ``popups`` list exceeds ``max_popups_count``, the oldest popup will be dismissed.
        max_popups_count: int = 3

    class Recorder(OptionsGroup):
        """
        Options for the :class:`~ignis.services.recorder.RecorderService`.
        """

        #: The bitrate of the recording.
        bitrate: int = 8000

        #: The default location for saving recordings. Defaults to XDG Video directory.
        default_file_location: str | None = get_recorder_default_file_location()

        #: The default filename for recordings. Supports time formating.
        default_filename: str = "%Y-%m-%d_%H-%M-%S.mp4"

    class Applications(OptionsGroup):
        """
        Options for the :class:`~ignis.services.applications.ApplicationsService`.
        """

        #: A list of the pinned applications desktop files, e.g. ``"firefox.desktop"``, ``"code.desktop"``.
        #:
        #: You shouldn't modify this option, use Application Service methods instead.
        pinned_apps: list[str] = []

    class Wallpaper(OptionsGroup):
        """
        Options for the :class:`~ignis.services.wallpaper.WallpaperService`.
        """

        #: The path to the wallpaper image.
        wallpaper_path: str | None = None

    notifications = Notifications()
    recorder = Recorder()
    applications = Applications()
    wallpaper = Wallpaper()


options = Options()
