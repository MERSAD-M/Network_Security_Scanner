import socket
from concurrent.futures import ThreadPoolExecutor
from target_resolver import ip_handler , port_handler


class TCPScanner:

    def __init__(self, timeout=2, threads=50):
        self.timeout = timeout
        self.threads = threads
    
    def port_scan(self , target : tuple):

        ip , port = target

        sock = None

        try:
            sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

            sock.settimeout(self.timeout)

            sock.connect(target)

            status = 'open'

        except ConnectionRefusedError:
            status = 'closed'

        except socket.timeout:
            status = 'timeout'

        except OSError:
            status = 'check network'

        finally:
            if sock:
                sock.close()

        return {
            'ip' : ip,
            'port' : port,
            'status' : status
        }
        
    def scan(self, ips, ports=None):            
        targets = list()
        if ports is None:
            ports = range(1 , 1024 + 1)
        for ip in ips:
            for port in ports:
                targets.append((ip , port))

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = list(executor.map(self.port_scan , targets))
        
        open_ports = [result for result in results if result['status'] == 'open']
        return open_ports


test = TCPScanner(threads=100)
for result in test.scan(ip_handler('192.168.1.1')):
    print(result)