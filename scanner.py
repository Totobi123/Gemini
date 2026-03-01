import socket

def grab_banner(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((host, port))
            # Initial grab
            banner = ""
            try:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except socket.timeout:
                # Nudge with HTTP if it timed out waiting for banner
                s.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            
            return banner if banner else "No banner received"
    except Exception as e:
        return f"Error: {e}"

def main():
    host = "127.0.0.1"
    ports = [22, 18789, 18791, 18792]
    print(f"Starting banner grabbing on {host}...")
    for port in ports:
        banner = grab_banner(host, port)
        print(f"Port {port}: {banner}")

if __name__ == "__main__":
    main()
