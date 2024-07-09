from scapy.all import *
import time

# Define source and destination IP addresses
src_ip="10.0.0.1"
dst_ip = "10.0.0.2"

# Define initial packet size in bytes
packet_size = 64

# Repeat the process 10 times
for iteration in range(10):
    # Variable to store the previous packets
    previous_packets = []

    # Send 20 packets with different source IP addresses and constant packet size
    for i in range(20):
        # Generate a random source IP address
        src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        
        # Create an IP packet with the specified source and destination IP addresses
        # and add 64-byte padding
        packet = IP(src=src_ip, dst=dst_ip) / ICMP()
        
        # Append the packet to the previous packets list
        previous_packets.append(packet)
        
        # Send the packets from the previous iteration
    for pkt in previous_packets:
        send(pkt)
        
        # Sleep for 10 seconds
    time.sleep(10)

   
