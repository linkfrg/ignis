import subprocess


def gst_inspect(name: str) -> bool:
    try:
        subprocess.run(["gst-inspect-1.0", "--exists", name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
