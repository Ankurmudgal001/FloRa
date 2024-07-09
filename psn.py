from scapy.all import *
import csv

def packet_sniffer(packet):
    # Extract relevant fields from the packet
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    protocol = packet[IP].proto
    timestamp = str(packet.time)

    # Write packet information to CSV file
    with open('packet_capture.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, src_ip, dst_ip, protocol])

# Sniff packets and call packet_sniffer function for each packet
sniff(prn=packet_sniffer, filter="ip", count=1000000)

print("Packet capture completed. Packets saved to packet_capture.csv.")

