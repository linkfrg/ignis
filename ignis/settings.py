import os
from gi.repository import GLib

CACHE_DIR = f"{GLib.get_user_cache_dir()}/ignis/"
os.makedirs(CACHE_DIR, exist_ok=True)