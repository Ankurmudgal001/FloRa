from scapy.all import *
from scapy import *
from scapy.utils import rdpcap
from scapy.utils import wrpcap

packets = rdpcap("/home/ankur/Desktop/univ1_pt2",count=2000)

for pkt in packets:
    if pkt.haslayer(IP) == 1:
        pkt[IP].src = "10.0.1.2"
        pkt[IP].dst = "10.0.1.3"
        del pkt[IP].chksum
#for pkt in packets:
 #pkt.display()

wrpcap("/home/ankur/Desktop/univ11_pt2.pcap", packets)
sendpfast(packets,iface="h2-eth0")
