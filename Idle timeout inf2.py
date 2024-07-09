from scapy.all import *
import time

src_ip = "192.168.1.10"
dst_ip_list = ["192.168.1.20", "192.168.1.30", "192.168.1.40", "192.168.1.50", "192.168.1.60"]
num_sends = 1000
delay = 8 # in seconds
rtt_list = []

for _ in range(num_sends):
    for dst_ip in dst_ip_list:
        icmp_packet = IP(src=dst_ip, dst=src_ip) / ICMP()
        start_time = time.time()
        response = send(icmp_packet)

        # Record the end time and calculate the RTT
        end_time = time.time()
        rtt = end_time - start_time
        rtt_list.append(rtt)

        # Print the RTT
        if response:
            print("Destination IP: {} | Round trip time: {:.6f} seconds".format(dst_ip, rtt))
        else:
            print("Destination IP: {} | No response received.".format(dst_ip))

       

    # Append an additional IP address to the dst_ip_list
    new_ip4 = "10.2.1.{}".format(len(dst_ip_list) + 2)
    new_ip5 = "10.2.{}.2".format(len(dst_ip_list) + 1)
    new_ip6 = "10.{}.2.{}".format(len(dst_ip_list) + 1,len(dst_ip_list) + 2)
    new_ip7 = "10.11.{}.{}".format(len(dst_ip_list) + 1,len(dst_ip_list) + 3)
    new_ip8 = "10.0.10.{}".format(len(dst_ip_list) + 2)
    new_ip9 = "10.0.{}.20".format(len(dst_ip_list) + 1)
    new_ip10 = "10.{}.10.{}".format(len(dst_ip_list) + 1,len(dst_ip_list) + 2)
    new_ip11 = "10.11.{}.{}".format(len(dst_ip_list) + 1,len(dst_ip_list) + 3)
    new_ip = "10.1.0.{}".format(len(dst_ip_list) + 2)
    new_ip1 = "10.1.{}.1".format(len(dst_ip_list) + 1)
    new_ip2 = "10.{}.11.{}".format(len(dst_ip_list) + 1,len(dst_ip_list) + 2)
    new_ip3 = "10.1.{}.{}".format(len(dst_ip_list) + 1,len(dst_ip_list) + 3)
    dst_ip_list.append(new_ip4)
    dst_ip_list.append(new_ip5)
    dst_ip_list.append(new_ip6)
    dst_ip_list.append(new_ip7)
    dst_ip_list.append(new_ip8)
    dst_ip_list.append(new_ip9)
    dst_ip_list.append(new_ip10)
    dst_ip_list.append(new_ip11)
    dst_ip_list.append(new_ip)
    dst_ip_list.append(new_ip1)
    dst_ip_list.append(new_ip2)
    dst_ip_list.append(new_ip3)
    # Delay before sending the next packet
    time.sleep(delay)

print("RTT list:", rtt_list)

