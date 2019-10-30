import asyncio
import aioping


async def do_ping(host):
    try:
        delay = await aioping.ping(host) * 1000
        print("Ping response in %s ms" % delay)

    except TimeoutError:
        print("Timed out")

loop = asyncio.get_event_loop()
loop.run_until_complete(do_ping("google.com"))
