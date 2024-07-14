from scapy.all import *

# Define the source and destination MAC addresses
src_mac = "00:00:00:00:00:01"
dst_mac = "00:00:00:00:00:02"

# Define the source and destination IP addresses
src_ip = "10.0.0.1"
dst_ip = "10.0.0.2"

# Define a list of packets to send
packets = [
    Ether(src=src_mac, dst=dst_mac)/IP(src=src_ip, dst=dst_ip)/ICMP(),
    Ether(src=src_mac, dst=dst_mac)/IP(src=src_ip, dst=dst_ip)/TCP(),
    Ether(src=src_mac, dst=dst_mac)/IP(src=src_ip, dst=dst_ip)/UDP()
]

# Send each packet in the list with a 1 second delay between packets
for packet in packets:
    sendp(packet, iface="eth0")
    time.sleep(1)
