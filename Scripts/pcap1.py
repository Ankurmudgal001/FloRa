from scapy.all import *
import time

batch_size = 10
delay = 1

packets = rdpcap("/home/ankur/Desktop/univ1_pt2")
print(packets)
total_packets = len(packets)
start_index = 0

while start_index < total_packets:
    end_index = min(start_index + batch_size, total_packets)
    current_packets = packets[start_index:end_index]

    for pkt in current_packets:
        if pkt.haslayer(IP):
            pkt[IP].src = "10.0.1.2"
            pkt[IP].dst = "10.0.1.3"
            del pkt[IP].chksum

    wrpcap("/home/ankur/Desktop/univ11_pt3", current_packets)
    sendpfast(current_packets, iface="h2-eth0")

    start_index += batch_size

    if start_index < total_packets:
        time.sleep(delay)


