from scapy.all import *
import time
import random

src_ip = "192.168.1.10"
dst_ip_list = "192.168.1.20"
num_sends = 1000
rtt_list = []

for _ in range(num_sends):
    for dst_ip in dst_ip_list:
        icmp_packet = IP(src=dst_ip, dst=src_ip) / ICMP()
        packet_size = random.randint(42, 120)  # Random packet size between 42 to 120 bytes
        icmp_packet = IP(src=src_ip, dst=dst_ip) / ICMP() / Raw(load=''.zfill(packet_size))

        start_time = time.time()
        response = send(icmp_packet)

        # Record the end time and calculate the RTT
        end_time = time.time()
        rtt = end_time - start_time
        rtt_list.append(rtt)

        # Print the RTT
        if response:
            print("Destination IP: {} | Packet Size: {} bytes | Round trip time: {:.6f} seconds".format(dst_ip, packet_size, rtt))
        else:
            print("Destination IP: {} | Packet Size: {} bytes | No response received.".format(dst_ip, packet_size))

    # Append an additional IP address to the dst_ip_list
    new_ip = "192.168.1.{}".format(len(dst_ip_list) + 2)
    dst_ip_list.append(new_ip)

    # Generate a random delay between 0 to 20 seconds
    delay = random.uniform(0, 20)
    # Delay before sending the next packet
    time.sleep(delay)

print("RTT list:", rtt_list)

