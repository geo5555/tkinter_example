import concurrent.futures
from ipaddress import ip_network, ip_address
import platform
import subprocess
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *

window = Tk()
window.title("Ping addresses on subnet")
frame1 = Frame(window)
frame1.grid(column=0, row=1)
LblSubnet = Label(frame1, text="Subnet:")
LblSubnet.grid(column=0, row=1)

txtSubnet = Entry(frame1, width=20)
txtSubnet.insert(0, "192.168.2.0/24")
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
            return False, ip
        else:
            return True, ip
    elif ping_reply.returncode == 1:
        return False, ip


def ping_all():
    text.delete(1.0, END)
    txtArea1.delete(1.0, END)
    subnet = txtSubnet.get()
    ip_list = [str(ip) for ip in ip_network(subnet).hosts()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        txtArea1.tag_configure('color1', foreground='green',
                       font=('Tempus Sans ITC', 12, 'bold'))
        txtArea1.tag_configure('color2', foreground='red',
                       font=('Tempus Sans ITC', 12, 'bold'))
        for ip in ip_list:
            future = executor.submit(ping_ip, ip)
            futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                if data[0]:
                    txtArea1.insert(END, data[1], 'color1')
                else:
                    txtArea1.insert(END, data[1], 'color2')
                txtArea1.insert(END, '\n')
                txtArea1.update()
            except Exception as exc:
                print('generated an exception: %s' % (exc))
            else:
                print((str(data)))

btnPing = Button(
    frame1, text="Ping all IPs in subnet", command=ping_all)
btnPing.grid(column=2, row=1)

window.mainloop()
