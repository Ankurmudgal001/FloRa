from scapy.all import *

destination_ip = "10.0.0.2"  # Replace with the actual destination IP address
interface_name = "h1-eth0"  # Replace with the correct network interface name

def send_icmp_packets():
    for i in range(1000):
        # Create an ICMP packet
        packet = IP(dst=destination_ip, tos=i % 256) / ICMP()

        # Send the packet
        send(packet, verbose=False, iface=interface_name)

    print("Sent 1000 ICMP packets with unique flow rules.")

# Send ICMP packets every 10 seconds
while True:
    send_icmp_packets()
    time.sleep(10)

