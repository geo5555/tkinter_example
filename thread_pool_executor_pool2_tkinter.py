import concurrent.futures
from ipaddress import ip_network, ip_address
import platform
import subprocess
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
from tkinter import messagebox

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
txtArea2 = scrolledtext.ScrolledText(window, width=50, height=30)
txtArea2.grid(column=1, row=2)

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
    txtArea1.delete(1.0, END)
    txtArea2.delete(1.0, END)
    subnet = txtSubnet.get()
    ip_list = [str(ip) for ip in ip_network(subnet).hosts()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        txtArea2.tag_configure('green', foreground='green',
                       font=('Tempus Sans ITC', 12, 'bold'))
        txtArea1.tag_configure('red', foreground='red',
                       font=('Tempus Sans ITC', 12, 'bold'))
        result = executor.map(ping_ip, ip_list)
        for data in result:
            if data[0]:
                txtArea2.insert(END, data[1], 'green')
                txtArea2.insert(END, '\n')
                txtArea2.update()
            else:
                txtArea1.insert(END, data[1], 'red')
                txtArea1.insert(END, '\n')
                txtArea1.update()
        messagebox.showinfo("Info", "Ping finished")

btnPing = Button(
    frame1, text="Ping all IPs in subnet", command=ping_all)
btnPing.grid(column=2, row=1)


window.mainloop()
