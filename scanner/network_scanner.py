from host_discover import HostDiscover
from target_resolver import ip_handler , port_handler
from tcp import TCPScanner

class NetworkScanner:

    def __init__(self , timeout=2, threads=50 , interval=1 , count=4):
        self.timeout = timeout
        self.threads = threads
        self.interval = interval
        self.count = count
        self.tcp_scanner = TCPScanner(threads=self.threads , timeout=self.timeout)
        self.host_discover = HostDiscover(timeout=self.timeout , threads=self.threads , interval=self.interval , count=self.count)

    def run(self , ips , ports=None):
        #port handler
        if ports is None:
            ports = range(1 , 1024 + 1)
        else:
            ports = port_handler(ports)
        #ip handler
        ips = ip_handler(ips)
        #host discover 
        hosts = self.host_discover.scan(ips)
        alive_hosts = []
        for host in hosts:
            if host['status'] == 'Up':
                alive_hosts.append(host['ip'])
        #network scan
        scan = self.tcp_scanner.scan(alive_hosts , ports)
        results = [result for result in scan if result['status'] == 'open']
        return results
    
test = NetworkScanner(count=2 , threads=200)
for r in test.run('192.168.1.0/24'):
    print(r)

