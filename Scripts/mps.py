from scapy.all import *
import random

dst_ip = "10.0.0.2"  # destination IP address
src_ip = "10.0.0.1"  # source IP address

# Generate 1000 different ICMP packets with random payload
packets = []
for i in range(10):
    payload = "".join([chr(random.randint(0, 255)) for j in range(64)])
    packet = IP(dst=dst_ip, src=src_ip)/ICMP()/Raw(load=payload)
    packets.append(packet)

# Send packets with different inter-packet interval
for i, packet in enumerate(packets):
    send(packet)
    if i < len(packets)-1:
        interval = random.uniform(0.1, 1.0)
        time.sleep(interval)
        print("Packet {}: Interval = {:.3f} seconds".format(i+1, interval))

