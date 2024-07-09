from scapy.all import *
import time
import csv

src_ip = "10.0.0.1"
dst_ip_list = ["10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6", "10.0.0.7", "10.0.0.8", "10.0.0.9", "10.0.0.10"]
num_sends = 10
delay = 3  # in seconds
rtt_list = []

while True:
    for dst_ip in dst_ip_list:
        icmp_packet = IP(src=src_ip, dst=dst_ip) / ICMP()
        start_time = time.time()
        response = sr1(icmp_packet, timeout=1)

        # Record the end time and calculate the RTT
        end_time = time.time()
        rtt = end_time - start_time
        rtt_list.append((icmp_packet, rtt))  # Store packet and RTT

        # Print the RTT
        if response:
            print("Destination IP: {} | Round trip time: {:.6f} seconds".format(dst_ip, rtt))
        else:
            print("Destination IP: {} | No response received.".format(dst_ip))

        # Delay before sending the next packet
        time.sleep(delay)

    # Check if the desired number of sends is reached
    if len(rtt_list) >= num_sends * len(dst_ip_list):
        break

    # Delay before resending the packets
    print("Resending packets in 10 seconds...")
    time.sleep(10)

# Save the RTT list as a CSV file
filename = "rtt_data.csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Packet", "RTT"])  # Write header
    for packet, rtt in rtt_list:
        writer.writerow([packet.summary(), rtt])  # Write packet summary and RTT

print("RTT list saved as", filename)

