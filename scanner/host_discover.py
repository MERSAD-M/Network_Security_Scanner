from icmplib import ping
from icmplib import SocketPermissionError
from icmplib import DestinationUnreachable
from concurrent.futures import ThreadPoolExecutor

class HostDiscover:

    def __init__(self , count=4 , timeout=2 , interval=1 , threads=50):
        self.count = count
        self.timeout = timeout
        self.interval = interval
        self.threads = threads

    def host_scan(self , ip):
        result = {
            'ip' : ip,
            'status' : None,
            'error' : None
        }
        try:
            host = ping(ip , count=self.count , interval=self.interval , timeout=self.timeout)
            if host.is_alive:
                result['status'] = 'Up' 

                result["details"] = {
                    "avg_rtt": host.avg_rtt,
                    "min_rtt": host.min_rtt,
                    "max_rtt": host.max_rtt,
                    "packet_loss": host.packet_loss
                }

            else:
                result['status'] = 'no_response'

        except DestinationUnreachable as e:
            result['status'] = 'network unreachable'

            result['error'] = {
                'type' : 'DestinationUnreachable',
                'message' : str(e)
            }

        except SocketPermissionError as e:
            result['status'] = 'permission denied'

            result['error'] = {
                'type' : 'SocketPermissionError',
                'message' : str(e)
            }
        except OSError as e:
            result['status'] = 'os error'

            result['error'] = {
                'type' :  type(e).__name__,
                'message' : str(e)
            }

        except Exception as e:
            result['status'] = 'unknown error'
            result['error'] = {
            'type': type(e).__name__,
            'message': str(e)
        }
        return result
    
    def scan(self , ips):

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = list(executor.map(self.host_scan , ips))
        return results

