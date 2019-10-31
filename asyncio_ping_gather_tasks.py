import asyncio
import aioping
import time
from ipaddress import ip_network, ip_address


async def safe_ping(ip, sem):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await do_ping(ip)


async def do_ping(host):
    try:
        delay = await aioping.ping(host, timeout=2) * 1000
        print("Ping response in %s ms" % delay)
        return host, delay
    except TimeoutError:
        print("Timed out")
        return host, "time out"


async def main():
    sem = asyncio.Semaphore(50)
    ip_list = [str(ip) for ip in ip_network("192.168.2.0/24").hosts()]

    tasks = [
        # asyncio.ensure_future(safe_download(url)) for url in urls
        asyncio.create_task(safe_ping(ip, sem)) for ip in ip_list
    ]
    t1 = time.perf_counter()
    results = await asyncio.gather(*tasks)  # await all downloads done
    t2 = time.perf_counter()
    print(t2-t1)
    for result in results:
        print(result)

asyncio.run(main())
