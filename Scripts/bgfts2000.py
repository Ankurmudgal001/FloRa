from scapy.all import *
from scapy.utils import rdpcap, wrpcap
import subprocess

# Load packets from the given pcap file
packets = rdpcap("/home/ankur/Desktop/univ1_pt2.pcap", count=2000)

# Modify IP addresses in the packets
for pkt in packets:
    if pkt.haslayer(IP):
        pkt[IP].src = "192.168.1.10"
        pkt[IP].dst = dst_list
        del pkt[IP].chksum

# Write the modified packets to a new pcap file
modified_pcap_path = "/home/ankur/Desktop/univ11_pt2.pcap"
wrpcap(modified_pcap_path, packets)

# Use tcpreplay to send the modified packets with a specified rate
iface = "h2-eth0"
pps = 300

tcpreplay_cmd = [
    "sudo", "tcpreplay",
    "--intf1={}".format(iface),
    "--pps={}".format(pps),
    modified_pcap_path
]

# Execute the tcpreplay command
subprocess.run(tcpreplay_cmd)

