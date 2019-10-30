from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
from ipaddress import ip_network, ip_address
from multiprocessing.dummy import Pool as ThreadPool
import time
import datetime
import threading
import platform
import subprocess

window = Tk()
window.title("Ping addresses on subnet")
frame1 = Frame(window)
frame1.grid(column=0, row=1)
LblSubnet = Label(frame1, text="Subnet:")
LblSubnet.grid(column=0, row=1)

txtSubnet = Entry(frame1, width=20)
txtSubnet.insert(0, "192.168.2.0/28")
txtSubnet.grid(column=1, row=1)


txtArea1 = scrolledtext.ScrolledText(window, width=50, height=30)
txtArea1.grid(column=0, row=2)
text = Text(window, width=80, height=30)
text.grid(column=1, row=2)


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
        print("\n* No response from device %s." % ip)
        return False, ip


def ping_all():
    text.delete(1.0, END)
    subnet = txtSubnet.get()
    numOfThreads = 40
    ip_list = list(ip_network(subnet).hosts())
    ip_list = [str(ip) for ip in ip_list]
    starttime = datetime.datetime.now()
    pool = ThreadPool(numOfThreads)
    results = pool.map(ping_ip, ip_list)
    pool.close()
    pool.join()
    text.tag_configure('color1', foreground='green',
                       font=('Tempus Sans ITC', 12, 'bold'))
    text.tag_configure('color2', foreground='red',
                       font=('Tempus Sans ITC', 12, 'bold'))
    for item in results:
        if item[0]:
            text.insert('end', item[1], 'color1')
        else:
            text.insert(END, item[1], 'color2')
        text.insert('end', '\n')
    totaltime = datetime.datetime.now() - starttime


btnPing = Button(
    frame1, text="Ping all IPs in subnet", command=ping_all)
btnPing.grid(column=2, row=1)

window.mainloop()
