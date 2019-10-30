import concurrent.futures
import urllib.request
from ipaddress import ip_network, ip_address
import platform
import subprocess

ip_list = list(ip_network("192.168.2.0/28").hosts())
ip_list = [str(ip) for ip in ip_list]

# Retrieve a single page and report the URL and contents


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
            # txtArea1.insert('end', "No response from device %s" % ip)
            # txtArea1.insert('end', '\n')
            return False, ip
        else:
            # txtArea1.insert('end', "OK response from device %s" % ip)
            # txtArea1.insert('end', '\n')
            return True, ip
    elif ping_reply.returncode == 1:
        # txtArea1.insert('end', "No response from device %s" % ip)
        # txtArea1.insert('end', '\n')
        #print("\n* No response from device %s." % ip)
        return False, ip


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Start the load operations and mark each future with its URL
    future_to_ping = {executor.submit(ping_ip, ip): ip for ip in ip_list}
    for future in concurrent.futures.as_completed(future_to_ping):
        ip = future_to_ping[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%s generated an exception: %s' % (ip, exc))
        else:
            print('%s page is %s' % (ip, str(data)))
