from scapy.all import *
import random
import time

# Define the source and destination IP addresses
src_ip = "10.0.0.1"
dst_ip = "10.0.0.2"

# Define the number of packets to send
num_packets = 10

# Send the packets with a random time interval between each packet
for i in range(num_packets):
    # Create the packet
    pkt = IP(src=src_ip, dst=dst_ip) / ICMP()
    
    # Record the current time
    send_time = time.time()
    
    # Send the packet
    send(pkt)
    
    # Wait for a random time interval between 1 and 5 seconds
    wait_time = random.uniform(1, 10)
    time.sleep(wait_time)
    
    # Calculate and print the interval between the packets
    recv_time = time.time()
    interval = recv_time - send_time
    print("Packet {}: Interval = {:.3f} seconds".format(i+1, interval))
    

