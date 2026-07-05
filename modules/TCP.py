import socket
from target_resolver import ip_handler , port_handler


class TCPScanner:

    def __init__(self, timeout=2, threads=50):
        self.timeout = timeout
        self.threads = threads

    def scan(self, ip, ports=None):
        results = []

        if ports is None:
            ports = range(1,1024+1)

        for ip_address in ip:
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)

                try:
                    sock.connect((ip_address, port))
                    status = "open"

                except socket.timeout:
                    status = "timeout"

                except OSError:
                    status = "closed"

                finally:
                    sock.close()

                results.append({
                    "ip": ip_address,
                    "port": port,
                    "status": status
                })

        return results
