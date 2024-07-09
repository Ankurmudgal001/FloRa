from scapy.all import *
import time
import os
# Define the source and destination MAC addresses
#src_mac = "00:00:00:00:00:01"
#dst_mac = "00:00:00:00:00:02"

# Define the source and destination IP addresses
src_ip = "192.168.1.10"
dst_ip = "192.168.1.20"
temp_dest_ip=[]
num_sends = 100
delay = 1  # in seconds
rtt_list=[]
for di in range(2,11):
	prefix="10.0.0."
	suffix=str(di)
	dip=prefix+suffix
	icmp_packet = IP(src=src_ip, dst=dip)/ICMP()
	start_time = time.time()
	response = sr1(icmp_packet, timeout=1)

	    # Record the end time and calculate the RTT
	end_time = time.time()
	rtt = end_time - start_time
	rtt_list.append(rtt)

	    # Print the RTT
	if response:
		print("Round trip time: {:.6f} seconds".format(rtt))
	else:
		print("No response received.")

	    # Delay before sending the next packet
	time.sleep(delay)

	
print(rtt_list)	


	
	


# Define the packet
#icmp_packet = IP(src=src_ip, dst=dst_ip)/ICMP()

# Define the number of times to send the packet and the delay between each send


# Send the packet multiple times with a delay between each send






