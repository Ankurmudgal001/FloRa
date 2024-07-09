from scapy.all import *

# Define the source and destination MAC addresses
src_mac = "00:00:00:00:00:01"
dst_mac = "00:00:00:00:00:02"

# Define the source and destination IP addresses
src_ip = "10.0.0.1"
dst_ip = "10.0.0.2"

# Define the packet
packet = Ether(src=src_mac, dst=dst_mac)/IP(src=src_ip, dst=dst_ip)/ICMP()

# Send the packet and record the start time
start_time = time.time()
response = sr1(packet, iface="eth0", timeout=1)

# Record the end time and calculate the RTT
end_time = time.time()
rtt = end_time - start_time

# Print the RTT
if response:
    print(f"Round trip time: {rtt:.6f} seconds")
else:
    print("No response received.")

