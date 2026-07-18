import re
import ipaddress

CIDR_PATTERN = re.compile(r'^(\d{1,3}(\.\d{1,3}){3})/(\d{1,2})$')
IP_PATTERN = re.compile(r'^(\d{1,3}(\.\d{1,3}){3})$')


def ip_handler(target: str) -> list[str]:
    target = target.strip()

    if CIDR_PATTERN.match(target):
        network = ipaddress.ip_network(target, strict=False)
        return [str(ip) for ip in network.hosts()]

    if IP_PATTERN.match(target):
        ipaddress.ip_address(target)  
        return [target]

    raise ValueError("Invalid IP or CIDR format")

SINGLE_PORT = re.compile(r'^\d+$')
RANGE_PORTS = re.compile(r'^\d+-\d+$')
CUSTOM_PORTS = re.compile(r"^\d+(,\d+)*$")

def port_handler(port : str):
    ports = []
    port = port.replace(' ' , '')
    if SINGLE_PORT.fullmatch(port):
        ports.append(int(port))
        return ports
    
    if RANGE_PORTS.fullmatch(port):
        RPORT = port.split('-')
        for p in range(int(RPORT[0]) , int(RPORT[1]) + 1):
            ports.append(p)
        return ports
    
    if CUSTOM_PORTS.fullmatch(port):
        CPORT = port.split(',')
        for p in CPORT:
            ports.append(int(p))
        return ports
        