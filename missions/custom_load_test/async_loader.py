import aiohttp
import asyncio
import argparse
import sys
import time
from fake_useragent import UserAgent

# -------------------------------------------------------------------------
# SAFETY NOTICE:
# This script is intended for AUTHORIZED LOAD TESTING and STRESS TESTING
# of systems you explicitly own or have permission to audit.
# Unauthorized use against third-party systems is illegal and unethical.
# -------------------------------------------------------------------------

async def fetch(session, url, counter):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        async with session.get(url, headers=headers) as response:
            status = response.status
            # Read the response to ensure the request completes
            await response.read()
            if status == 200:
                print(f"[+] Request {counter}: Success (200)")
            else:
                print(f"[-] Request {counter}: Failed ({status})")
            return status
    except Exception as e:
        print(f"[!] Request {counter}: Error - {str(e)}")
        return 0

async def bound_fetch(sem, session, url, counter):
    # Semaphore limits concurrency to prevent local resource exhaustion
    async with sem:
        return await fetch(session, url, counter)

async def run_load_test(url, total_requests, concurrency):
    print(f"[*] Starting load test on: {url}")
    print(f"[*] Total Requests: {total_requests}")
    print(f"[*] Concurrency Level: {concurrency}")
    
    tasks = []
    sem = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:
        for i in range(total_requests):
            task = asyncio.ensure_future(bound_fetch(sem, session, url, i+1))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
    success_count = responses.count(200)
    print("
[=] Load Test Complete")
    print(f"[=] Successful Requests: {success_count}/{total_requests}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async Load Testing Tool (Educational)")
    parser.add_argument("url", help="Target URL (e.g., http://localhost:8080)")
    parser.add_argument("-n", "--requests", type=int, default=100, help="Total number of requests")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent requests")

    args = parser.parse_args()

    # Basic URL validation
    if not args.url.startswith("http"):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    start_time = time.time()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_load_test(args.url, args.requests, args.concurrency))
    except KeyboardInterrupt:
        print("
[!] Test interrupted by user.")
    finally:
        end_time = time.time()
        print(f"[=] Duration: {end_time - start_time:.2f} seconds")
