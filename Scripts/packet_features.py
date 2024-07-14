from scapy.all import *
import csv
import time

packet_count = 0
packet_intervals = []
match_bytes = []
flow_rules = {}

def packet_sniffer(packet):
    global packet_count, packet_intervals, match_bytes, flow_rules

    # Get current timestamp
    timestamp = time.time()

    # Calculate packet interval and update packet_intervals list
    if packet_count > 0:
        interval = timestamp - packet_intervals[-1]
        packet_intervals.append(timestamp)
    else:
        interval = 0
        packet_intervals.append(timestamp)

    # Update match_bytes list
    match_bytes.append(len(packet))

    # Check if flow rule duration exists for the packet
    if packet_count in flow_rules:
        duration = timestamp - flow_rules[packet_count]
    else:
        duration = 0

    # Update flow rule duration for the packet
    flow_rules[packet_count] = timestamp

    # Increment packet count
    packet_count += 1

    # Print packet details
    print("Packet #{}".format(packet_count))
    print("Duration of flow rule: {}".format(duration))
    print("Relative dispersion of match bytes: {}".format(calculate_relative_dispersion(match_bytes)))
    print("Total number of packets matched with flow rules: {}".format(packet_count))
    print("Relative dispersion of packet interval in SDN: {}".format(calculate_relative_dispersion(packet_intervals)))
    print("-" * 50)

    # Write packet information to CSV file
    with open('packet_capture.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([packet_count, duration, calculate_relative_dispersion(match_bytes), packet_count, calculate_relative_dispersion(packet_intervals)])

def calculate_relative_dispersion(data):
    if len(data) <= 1:
        return 0
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance / mean

# Sniff packets and call packet_sniffer function for each packet
sniff(prn=packet_sniffer, filter="ip", count=1000)

print("Packet capture completed. Packets saved to packet_capture.csv.")

