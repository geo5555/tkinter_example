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
    # Start the load operations and mark each future with its ip
    future_to_ping = {executor.submit(ping_ip, ip): ip for ip in ip_list}
    print(future_to_ping)
    for future in concurrent.futures.as_completed(future_to_ping):
        ip = future_to_ping[future] #get the ip from the dictionary we created earlier
        try:
            data = future.result() #get the result
        except Exception as exc:
            print('%s generated an exception: %s' % (ip, exc))
        else:
            print('%s page is %s' % (ip, str(data)))
