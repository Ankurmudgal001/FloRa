from scapy.all import *
import time

# Define the destination IP address
destination_ip = "10.0.0.2"

# Define the number of packets to send
num_packets = 3

# List to store round trip times
rtt_list = []

# Define the packets
packets = [
    IP(dst=destination_ip) / ICMP(),
    IP(dst=destination_ip) / TCP(),
    IP(dst=destination_ip) / UDP(),
    # Add more packets here...
]

# Send packets and record round trip time
for i in range(num_packets):
    packet = packets[i % len(packets)]  # Select the next packet in a cyclic manner

    # Send packet and capture response
    start_time = time.time()
    reply = sr1(packet, verbose=0)
    end_time = time.time()

    # Calculate round trip time
    rtt = end_time - start_time

    # Add round trip time to the list
    rtt_list.append(rtt)

    # Print round trip time
    print("Packet {} RTT: {} seconds".format(i+1, rtt))

    # Wait for 1 second before sending the next packet
    time.sleep(1)

# Print the list of round trip times
print("RTT list:", rtt_list)

