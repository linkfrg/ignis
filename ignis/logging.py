import os
import sys
from loguru import logger
from gi.repository import GLib  # type: ignore

LOG_DIR = os.path.expanduser("~/.ignis")
LOG_FILE = f"{LOG_DIR}/ignis.log"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} [<level>{level}</level>] {message}"


G_LOG_LEVEL_FUNC = {
    GLib.LogLevelFlags.LEVEL_DEBUG: lambda message: logger.debug(message),
    GLib.LogLevelFlags.LEVEL_MESSAGE: lambda message: logger.trace(message),
    GLib.LogLevelFlags.LEVEL_INFO: lambda message: logger.info(message),
    GLib.LogLevelFlags.LEVEL_WARNING: lambda message: logger.warning(message),
    GLib.LogLevelFlags.LEVEL_ERROR: lambda message: logger.error(message),
    GLib.LogLevelFlags.LEVEL_CRITICAL: lambda message: logger.critical(message),
}


def logging_excepthook(exc_type, exc_value, exc_traceback):
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).error(
        f"{exc_type.__name__}: {exc_value}"
    )


def g_log_writer(
    logs_level: GLib.LogLevelFlags, log_fields: list[GLib.LogField], gsize: int
) -> GLib.LogWriterOutput:
    message = GLib.log_writer_format_fields(logs_level, log_fields, False)

    # debug and info messages usually useless
    if logs_level == GLib.LogLevelFlags.LEVEL_DEBUG:
        ...
    elif logs_level == GLib.LogLevelFlags.LEVEL_INFO:
        ...
    else:
        func = G_LOG_LEVEL_FUNC.get(logs_level, None)
        if func is not None:
            func(message.strip())

    return GLib.LogWriterOutput.HANDLED


def configure_logger(debug: bool) -> None:
    logger.remove()

    if debug:
        LEVEL = "DEBUG"
    else:
        LEVEL = "INFO"

    logger.add(sys.stderr, colorize=True, format=LOG_FORMAT, level=LEVEL)
    logger.add(LOG_FILE, format=LOG_FORMAT, level=LEVEL, rotation="1 day")

    logger.level("INFO", color="<green>")

    sys.excepthook = logging_excepthook

    GLib.log_set_writer_func(g_log_writer)
