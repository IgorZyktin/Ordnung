import os
import socket


def get_local_ip() -> str:
    """Find out which local IP is, so we can broadcast to the LAN.
    """
    if os.name == 'nt':
        ip = socket.gethostbyname(socket.gethostname())

    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # noinspection PyBroadException
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()

    return ip