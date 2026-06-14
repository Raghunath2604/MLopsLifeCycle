import asyncio
import aiohttp
import time

url = "http://a3fef5535b8f14a05a6aa3306ab88040-1540167051.us-east-2.elb.amazonaws.com/"

async def fetch(session):
    async with session.get(url) as response:
        return response.status

async def run_load_test():
    async with aiohttp.ClientSession() as session:
        print("[+] Commencing DDoS simulation against MLOps Cluster...")
        print(f"Target URL: {url}")
        print("Firing 50 simultaneous requests in 1 second...\n")
        
        start = time.time()
        tasks = [fetch(session) for _ in range(50)]
        results = await asyncio.gather(*tasks)
        end = time.time()
        
        from collections import Counter
        status_counts = Counter(results)
        
        print(f"RESULTS OF 50 SIMULTANEOUS REQUESTS:")
        print(f"Time Elapsed: {(end-start):.2f} seconds")
        print(f"Status Counts: {dict(status_counts)}")
        
        if status_429 > 0:
            print("\nVERDICT: NGINX DDoS Protection is ACTIVE and successfully intercepting attacks!")
        else:
            print("\nVERDICT: Rate limiting failed to block traffic.")

if __name__ == "__main__":
    asyncio.run(run_load_test())
