from scapy.all import *

# Define source and destination IP addresses
src_ip = "10.0.0.1"
dst_ip = "10.0.0.2"

# Define packet size in bytes
packet_size = 64

# Send 20 packets with different source IP addresses and 64-byte padding
for i in range(20):
    # Generate a random source IP address
    src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
    
    # Create an IP packet with the specified source and destination IP addresses
    # and add 64-byte padding
    packet = IP(src=src_ip, dst=dst_ip) / Padding(load="X" * (packet_size - 20))
    
    # Send the packet
    send(packet)

