from scapy.all import *
from scapy.utils import rdpcap
from scapy.utils import wrpcap

packets = rdpcap("/home/ankur/Desktop/univ1_pt2", count=20000)
source_ips = ["10.0.1.2","10.0.1.4","10.0.1.5","10.0.1.6","10.0.1.7","10.0.1.8","10.0.1.9","10.0.1.10","10.0.1.11","10.0.1.12","10.0.1.13","10.0.1.14","10.0.1.15","10.0.1.16","10.0.1.17","10.0.1.18","10.0.1.19","10.0.1.1"]  # List of source IP addresses

for i, pkt in enumerate(packets):
    if pkt.haslayer(IP):
        pkt[IP].src = source_ips[i % len(source_ips)]  # Assign source IP in a round-robin fashion
        pkt[IP].dst = "10.0.1.3"  # Destination IP
        del pkt[IP].chksum

wrpcap("/home/ankur/Desktop/univ111_pt2.pcap", packets)
sendp(packets, iface="h2-eth0")

