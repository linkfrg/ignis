from .application import Application
from gi.repository import Gio  # type: ignore


def search_apps(
    apps: list[Application],
    query: str,
) -> list[Application]:
    """
    Search applications by a query.

    Args:
        apps: A list of applications where to search, e.g., :attr:`~ignis.services.applications.ApplicationsService.apps`.
        query: The string to be searched for.

    Returns:
        list[Application]: A list of applications filtered by the provided query.
    """
    return [
        entry
        for result in Gio.DesktopAppInfo.search(query)
        for entry in apps
        if entry.id in result
    ]
