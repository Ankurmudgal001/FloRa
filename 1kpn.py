from scapy.all import *
import time

# Define the destination IP address
destination_ip = "10.0.0.2"

# Define the number of packets to send
num_packets = 10

# Define the interval between packet retransmissions (in seconds)
retransmission_interval = 10

# List to store round trip times
rtt_list = []

# Send packets and record round trip time
for _ in range(num_packets):
    # Craft packet (e.g., TCP packet)
    packet = IP(dst=destination_ip) / TCP()

    # Send packet and capture response
    start_time = time.time()
    reply = sr1(packet, verbose=0)
    end_time = time.time()

    # Calculate round trip time
    rtt = end_time - start_time

    # Add round trip time to the list
    rtt_list.append(rtt)

    # Wait for the retransmission interval
    time.sleep(retransmission_interval)

# Print the list of round trip times
print(rtt_list)

