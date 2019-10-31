import asyncio
import aioping
import time
from ipaddress import ip_network, ip_address


async def safe_ping(q):
    while True:
        ip = await q.get()
        if ip is None:
            # pass on the word that we're done, and exit
            await q.put(None)
            break
        a = await do_ping(ip)
        print(a)


async def do_ping(host):
    try:
        delay = await aioping.ping(host, timeout=2) * 1000
        print("Ping response in %s ms" % delay)
        return host, delay
    except TimeoutError:
        print("Timed out")
        return host, "time out"


async def main():
    q = asyncio.Queue()
    ip_list = [str(ip) for ip in ip_network("192.168.2.0/24").hosts()]
    t1 = time.perf_counter()
    workers = [asyncio.create_task(safe_ping(q)) for _ in range(50)]
    for ip in ip_list:
        await q.put(ip)
    await q.put(None)

    await asyncio.wait(workers)
    t2 = time.perf_counter()
    print(t2-t1)


asyncio.run(main())
