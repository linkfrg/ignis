def check_is_vpn(func):
    def wrapper(*args, **kwargs):
        connection = args[2]
        if (
            connection.get_connection_type() == "vpn"
            or connection.get_connection_type() == "wireguard"
        ):
            func(*args, **kwargs)

    return wrapper
