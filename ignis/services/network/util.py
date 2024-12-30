def check_is_vpn(func):
    def wrapper(*args, **kwargs):
        connection = args[2]
        if (
            connection.get_connection_type() == "vpn"
            or connection.get_connection_type() == "wireguard"
        ):
            func(*args, **kwargs)

    return wrapper


def get_wifi_connect_window_name(bssid: str) -> str:
    return f"wifi-connect_{bssid}"
