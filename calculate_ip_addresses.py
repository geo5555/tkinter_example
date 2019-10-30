from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
from ipaddress import ip_network, ip_address
import re
from jinja2 import Environment, FileSystemLoader
from pprint import pprint

window = Tk()
window.title("Calculate IP addresses by GE")
#window.geometry('1200x600')
frame1 = Frame(window)
frame1.grid(column=0, row=1)
txtSubnet = Entry(frame1, width=20)
txtSubnet.insert(0, "10.36.64.0/22")
txtSubnet.grid(column=1, row=1)
LblSubnet = Label(frame1, text="Subnet/22")
LblSubnet.grid(column=0, row=1)
txtWanIP = Entry(frame1, width=20)
lblWanIP = Label(frame1, text="Wan IP")
txtWanIP.insert(0, "172.16.34.66")
txtWanIP.grid(column=1, row=2)
lblWanIP.grid(column=0, row=2)
txtHostname = Entry(frame1, width=20)
lblHostname = Label(frame1, text="Hostname")
txtHostname.insert(0, "rtr1213")
txtHostname.grid(column=1, row=3)
lblHostname.grid(column=0, row=3)
txtTunnel20 = Entry(frame1, width=20)
lblTunnel20 = Label(frame1, text="tunnel20 IP")
txtTunnel20.insert(0, "10.12.12.13")
txtTunnel20.grid(column=1, row=4)
lblBW = Label(frame1, text="BW")
lblBW.grid(column=0, row=4)
choices = ['1Mb', '2MB', '4MB', '6MB', '10Mb', '15Mb', '20Mb']
bw1 = Combobox(frame1, values=choices)
bw1.current(1)
bw1.grid(column=1, row=4)
choices2 = ['2911', '4321', '881']
bw2 = Combobox(frame1, values=choices2)
bw2.current(0)
#print(type(bw2.current())) #int return index
bw2.grid(column=1, row=5)
txtArea1 = scrolledtext.ScrolledText(window, width=50, height=30)
txtArea1.grid(column=0, row=2)
txtArea2 = scrolledtext.ScrolledText(window, width=80, height=30)
txtArea2.grid(column=1, row=2)


def calculate():
    global directory1
    txtArea1.delete("1.0", END)
    txtArea2.delete("1.0", END)
    hostname = txtHostname.get()
    subnet = txtSubnet.get()
    wan_ip = txtWanIP.get()
    dict_form = { '1Mb':0, '2MB':1, '4MB':2, '6MB':3, '10Mb':4, '15Mb':5, '20Mb':6}
    pm_list = ['pm-mpls-1024-v3.1', 'pm-mpls-1920-v3.1', 'pm-mpls-4096-v3.1',
               'pm-mpls-6144-v3.1', 'pm-mpls-10240-v3.1', 'pm-mpls-15120-v3.1', 'pm-mpls-20MB-v3.1']
    bw = ['1024', '2048', '4096', '6144', '10240', '15120', '20000']
    qos_citr = ['qos-citr-1024-v3.1', 'qos-citr-2048-v3.1', 'qos-citr-4096-v3.1',
                'qos-citr-6144-v3.1', 'qos-citr-10240-v3.1', 'qos-citr-15120-v3.1',
                'qos-citr-20000-v3.1']
    qos = ['qos_1024.ios', 'qos_2048.ios', 'qos_4096.ios',
           'qos_6144.ios', 'qos_10240.ios', 'qos_15120.ios', 'qos_20000.ios']
    hostname = txtHostname.get()
    host = hostname[3:]
    hostname_b = 'rtrb'+host
    wan_ip = txtWanIP.get()
    wan_ip_across = ip_address(wan_ip)-1
    tunnel20ip = txtTunnel20.get()
    ip_subnet = txtSubnet.get()
    #service_policy_output = dict_form[bw2]
    #router_type = dict_form['router_type']
    service_policy_output = bw1.current()
    router_type = bw2.current()+1
    ip_net = ip_network(ip_subnet)
    ip_subnet_ip = ip_net.network_address
    ip_subnet_mask = ip_net.netmask
    ip_subnet_hostmask = ip_net.hostmask
    ipnets24 = list(ip_net.subnets(new_prefix=24))
    loopback0_ip, data_ip, data_ip_b, data_vrrp_ip, voice_ip, iprest = (
        ipnets24[0][1],
        ipnets24[1][6],
        ipnets24[1][5],
        ipnets24[1][1],
        ipnets24[2][1],
        ipnets24[3]
    )
    subs28 = list(ip_network(iprest).subnets(new_prefix=28))
    atm_ip, atm_ip_b, atm_vrrp_ip, guest_ip, bms_ip = (
        subs28[0][6],
        subs28[0][5],
        subs28[0][1],
        subs28[1][1],
        subs28[2][1]
    )
    remediation_ip, remediation_vrrp_ip = subs28[14][2], subs28[14][1]
    qosindex = int(service_policy_output)
    #router_type = int(router_type)

    net16 = ip_network("10.12.0.0/16")
    subs19 = list(ip_network(net16).subnets(new_prefix=19))
    tun20sub, tun21sub, tun22sub = subs19[0], subs19[1], subs19[6]
    tun110sub, tun112sub, tun212sub = subs19[2], subs19[7], subs19[3]
    tun20ip = ip_address(tunnel20ip)
    a = 1
    for i, addr in enumerate(tun20sub):
        if tun20ip == addr:
            a = i
            break
    tunnel21ip = tun21sub[a]
    tunnel22ip = tun22sub[a]
    tunnel110ip = tun110sub[a]
    tunnel112ip = tun112sub[a]
    tunnel212ip = tun212sub[a]

    context = {
        'aps2': subs28[0][13],
        'aps1': subs28[0][12],
        'atm1': subs28[0][9],
        'atm2': subs28[0][10],
        'atm3': subs28[0][11],
        'pos1': subs28[0][14],
        'pos2': subs28[0][15],
        'ip_subnet': ip_subnet,
        'ip_subnet_ip': ip_subnet_ip,
        'ip_subnet_mask': ip_subnet_mask,
        'ip_subnet_hostmask': ip_subnet_hostmask,
        'host': host,
        'hostname': hostname,
        'hostname_b': hostname_b,
        'wan_ip': wan_ip,
        'wan_ip_across': wan_ip_across,
        'data_ip': data_ip,
        'data_ip_b': data_ip_b,
        'data_vrrp_ip': data_vrrp_ip,
        'atm_ip': atm_ip,
        'atm_ip_b': atm_ip_b,
        'atm_vrrp_ip': atm_vrrp_ip,
        'bms_ip': bms_ip,
        'voice_ip': voice_ip,
        'guest_ip': guest_ip,
        'remediation_ip': remediation_ip,
        'remediation_vrrp_ip': remediation_vrrp_ip,
        'policy_map': pm_list[qosindex],
        'service_policy_template': 'router/snippets_2911/'+qos[qosindex],
        'bw': bw[qosindex],
        'qos_citr': qos_citr[qosindex],
        'tunnel20ip': tunnel20ip,
        'tunnel21ip': tunnel21ip,
        'tunnel22ip': tunnel22ip,
        'tunnel110ip': tunnel110ip,
        'tunnel112ip': tunnel112ip,
        'tunnel212ip': tunnel212ip,
        'loopback0_ip': loopback0_ip,
        'router_type': router_type
    }
    for key, value in sorted(context.items(),  key=lambda x: x[0]):
        txtArea1.insert('end', key+': '+str(value))
        txtArea1.insert('end', '\n')
    render_jinja2(context)

ENV = Environment(loader=FileSystemLoader('.'))

def render_jinja2(context):
    template = ENV.get_template('router2911.j2')
    result=template.render(context)
    txtArea2.insert('end',result)
    
btnCalculate = Button(
    frame1, text="Calculate", command=calculate)
btnCalculate.grid(column=0, row=6, columnspan=2)
window.mainloop()
