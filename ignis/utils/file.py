from gi.repository import Gio  # type: ignore


def _get_gfile(
    func_name: str,
    path: str | None = None,
    uri: str | None = None,
    gfile: "Gio.File | None" = None,
) -> Gio.File:
    if path:
        gfile = Gio.File.new_for_path(path)
    elif uri:
        gfile = Gio.File.new_for_uri(uri)
    elif gfile:
        pass
    else:
        TypeError(
            f"{func_name} requires either a path or an URI or a Gio.File to be provided"
        )

    return gfile  # type: ignore


def _get_contents(
    func_name: str, contents: bytes | None = None, string: str | None = None
) -> bytes:
    if string:
        contents = string.encode()
    elif contents:
        pass
    else:
        TypeError(f"{func_name} requires either contents or a string to be provided")

    return contents  # type: ignore


def read_file(
    path: str | None = None,
    uri: str | None = None,
    gfile: "Gio.File | None" = None,
    decode: bool = True,
) -> str | bytes:
    """
    Read the contents of a file.

    Args:
        path: The path to the file.
        uri: The URI of the file.
        gfile: An instance of :class:`Gio.File`.
        decode: Whether to decode the file's contents. If ``True``, this function will return :obj:`str`, otherwise :obj:`bytes`.

    Returns:
        The contents of the file.

    At least one of the arguments, ``path``, ``uri``, or ``gfile``, must be provided.

    Example usage:

    .. code-block:: python

        from ignis.utils import Utils

        # regular file
        contents = Utils.read_file(path="/path/to/file", decode=True)
        print(contents)

        # URI
        Utils.read_file(uri="file:///path/to/file", decode=True)
        # Web also supported
        Utils.read_file(uri="https://SOME_SITE.org/example_content", decode=False)
    """
    gfile = _get_gfile(func_name="read_file()", path=path, uri=uri, gfile=gfile)

    _, contents, _ = gfile.load_contents()
    if decode:
        return contents.decode()
    else:
        return contents


async def read_file_async(
    path: str | None = None,
    uri: str | None = None,
    gfile: "Gio.File | None" = None,
    decode: bool = True,
) -> None:
    """
    Asynchronously read the contents of a file.

    Args:
        path: The path to the file.
        uri: The URI of the file.
        gfile: An instance of :class:`Gio.File`.
        decode: Whether to decode the file's contents. If ``True``, the callback will receive :obj:`str`, otherwise :obj:`bytes`.
        callback: A function to call when the operation is complete. It will receive the file's contents (:obj:`bytes` or :obj:`str`).
        *user_data: User data to pass to ``callback``.

    At least one of the arguments, ``path``, ``uri``, or ``gfile``, must be provided.

    Example usage:

    .. code-block:: python

        from ignis.utils import Utils

        def some_callback(contents: bytes | str) -> None:
            print(contents)

        # regular file
        Utils.read_file_async(path="/path/to/file", decode=True, callback=some_callback)

        # URI
        Utils.read_file_async(uri="file:///path/to/file", decode=True, callback=some_callback)
        # Web also supported
        Utils.read_file_async(uri="https://SOME_SITE.org/example_content", decode=False, callback=some_callback)
    """
    gfile = _get_gfile(func_name="read_file_async()", path=path, uri=uri, gfile=gfile)

    _, contents, _ = await gfile.load_contents_async()  # type: ignore

    if decode:
        return contents.decode()
    else:
        return contents


def write_file(
    path: str | None = None,
    uri: str | None = None,
    gfile: "Gio.File | None" = None,
    contents: bytes | None = None,
    string: str | None = None,
) -> None:
    """
    Write contents to a file.

    Args:
        path: The path to the file.
        uri: The URI of the file.
        gfile: An instance of :class:`Gio.File`.
        contents: The bytes to write to the file.
        string: The string to write to the file.

    At least one of the arguments, ``path``, ``uri``, or ``gfile``, must be provided.
    Either ``contents`` or ``string`` must be provided.

    Example usage:

    .. code-block:: python

        from ignis.utils import Utils

        # write string
        Utils.write_file(path="/path/to/file", string="some_string")
        # or bytes
        Utils.write_file(path="/path/to/file", bytes=b"some bytes")
    """
    gfile = _get_gfile(func_name="write_file()", path=path, uri=uri, gfile=gfile)
    contents = _get_contents(func_name="write_file()", contents=contents, string=string)

    gfile.replace_contents(
        contents, None, False, Gio.FileCreateFlags.REPLACE_DESTINATION, None
    )


async def write_file_async(
    path: str | None = None,
    uri: str | None = None,
    gfile: "Gio.File | None" = None,
    contents: bytes | None = None,
    string: str | None = None,
) -> None:
    """
    Asynchronously write contents to a file.

    Args:
        path: The path to the file.
        uri: The URI of the file.
        gfile: An instance of :class:`Gio.File`.
        contents: The bytes to write to the file.
        string: The string to write to the file.
        callback: A function to call when the operation is complete.
        *user_data: User data to pass to ``callback``.

    At least one of the arguments, ``path``, ``uri``, or ``gfile``, must be provided.
    Either ``contents`` or ``string`` must be provided.

    Example usage:

    .. code-block:: python

        from ignis.utils import Utils

        def some_callback() -> None:
            print("Operation is complete")

        # write string
        Utils.write_file_async(path="/path/to/file", string="some_string", callback=some_callback)
        # or bytes
        Utils.write_file_async(path="/path/to/file", bytes=b"some bytes", callback=some_callback)
    """
    gfile = _get_gfile(func_name="write_file_async()", path=path, uri=uri, gfile=gfile)
    contents = _get_contents(
        func_name="write_file_async()", contents=contents, string=string
    )

    await gfile.replace_contents_async(   # type: ignore
        contents,
        None,
        False,
        Gio.FileCreateFlags.REPLACE_DESTINATION,
    )
