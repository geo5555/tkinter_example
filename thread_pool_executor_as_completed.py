import concurrent.futures
from ipaddress import ip_network, ip_address
import platform
import subprocess
import time

ip_list = [str(ip) for ip in ip_network("192.168.2.0/24").hosts()]


def checkPlatform(Name):
    return Name.lower() == platform.system().lower()


def ping_ip(ip):
    if checkPlatform("Windows"):
        ping_reply = subprocess.run(
            ["ping", "-n", "2", "-w", "2", ip], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
        ping_reply = subprocess.run(
            ["ping", "-c", "2", "-w", "2", ip], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if ping_reply.returncode == 0:
        if ("unreachable" in str(ping_reply.stdout)):
            return False, ip
        else:
            return True, ip
    elif ping_reply.returncode == 1:
        return False, ip


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    t1 = time.perf_counter()
    # Start the load operations and mark each future with its ip
    future_to_ping = {executor.submit(ping_ip, ip): ip for ip in ip_list}
    for future in concurrent.futures.as_completed(future_to_ping):
        # get the ip from the dictionary we created earlier
        ip = future_to_ping[future]
        try:
            data = future.result()  # get the result
        except Exception as exc:
            print('%s generated an exception: %s' % (ip, exc))
        else:
            print('%s result is: %s' % (ip, str(data)))
    t2 = time.perf_counter()
    print(t2-t1)
