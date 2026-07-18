import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import argparse
from scanner.network_scanner import NetworkScanner

parser = argparse.ArgumentParser(description='Network reconnaissance and port scanning tool')

parser.add_argument('-t' , '--target' , type=str , help='target IP address or CIDR range' , required=True)
parser.add_argument('-p' , '--ports' , type=str , help='ports to scan (examples: 80, 20-80, 21,80,443)')
parser.add_argument('--threads' , type=int , help='number of threads' , default=50)
parser.add_argument('-c' , '--count' , type=int , help='number of ICMP echo requests' , default=4)
parser.add_argument('-i' , '--interval' , type=float , help='time interval between ICMP echo requests' , default=1)
parser.add_argument('--timeout' , type=float , help='timeout in seconds' , default=2)

args = parser.parse_args()

scan = NetworkScanner(threads=args.threads , count=args.count , timeout=args.timeout , interval=args.interval)

result = scan.run(args.target , args.ports)

print(result)