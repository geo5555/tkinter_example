import concurrent.futures
from ipaddress import ip_network, ip_address
import platform
import subprocess

ip_list = [str(ip) for ip in ip_network("192.168.2.0/28").hosts()]


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
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for ip in ip_list:
        future = executor.submit(ping_ip, ip)
        futures.append(future)
    for future in concurrent.futures.as_completed(futures):
        try:
            data = future.result() 
        except Exception as exc:
            print('generated an exception: %s' % (exc))
        else:
            print((str(data)))
