from typing import TypeAlias
from .exec_sh import exec_sh, exec_sh_async
from .load_interface_xml import load_interface_xml
from .poll import Poll
from .get_monitor import get_monitor
from .get_n_monitors import get_n_monitors
from .timeout import Timeout
from .file_monitor import FileMonitor
from .thread import thread, run_in_thread
from .sass import sass_compile
from .get_ignis_version import (
    get_ignis_version,
    get_ignis_commit,
    get_ignis_branch,
    get_ignis_commit_msg,
)
from .scale_pixbuf import scale_pixbuf
from .crop_pixbuf import crop_pixbuf
from .get_paintable import get_paintable
from .get_file_icon_name import get_file_icon_name
from .thread_task import ThreadTask
from .download_image import download_image
from .get_current_dir import get_current_dir
from .socket import send_socket, listen_socket


class Utils:
    exec_sh = exec_sh
    exec_sh_async = exec_sh_async
    load_interface_xml = load_interface_xml
    Poll: TypeAlias = Poll
    get_monitor = get_monitor
    get_n_monitors = get_n_monitors
    Timeout: TypeAlias = Timeout
    FileMonitor: TypeAlias = FileMonitor
    thread = thread
    run_in_thread = run_in_thread
    sass_compile = sass_compile
    get_ignis_version = get_ignis_version
    scale_pixbuf = scale_pixbuf
    crop_pixbuf = crop_pixbuf
    get_paintable = get_paintable
    get_file_icon_name = get_file_icon_name
    ThreadTask: TypeAlias = ThreadTask
    get_ignis_commit = get_ignis_commit
    download_image = download_image
    get_current_dir = get_current_dir
    get_ignis_branch = get_ignis_branch
    get_ignis_commit_msg = get_ignis_commit_msg
    send_socket = send_socket
    listen_socket = listen_socket
