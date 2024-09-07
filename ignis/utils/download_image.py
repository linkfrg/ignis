import requests


def download_image(url: str, path: str, **kwargs) -> int:
    """
    Download an image from the given URL.

    Args:
        url (``str``): The URL of the image.
        path (``str``): The path where the image will be saved.

    kwargs will be passed to the ``requests.get()`` method.

    Returns:
        ``int``: The response status code (``200`` if success).
    """
    response = requests.get(url, **kwargs)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)

    return response.status_code
