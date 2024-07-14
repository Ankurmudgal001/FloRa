from scapy.all import send, IP, ICMP, TCP, UDP
import random
import time

# Function to generate a random IP address
def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Function to generate packets with different protocols
def generate_packets(num_packets, destinations):
    packets = []
    for _ in range(num_packets):
        src_ip = random_ip()
        dst_ip = random.choice(destinations)
        
        # Choose a random protocol (ICMP, TCP, UDP)
        protocol = random.choice(['ICMP', 'TCP', 'UDP'])
        
        if protocol == 'ICMP':
            packet = IP(src=src_ip, dst=dst_ip) / ICMP()
        elif protocol == 'TCP':
            src_port = random.randint(1024, 65535)
            dst_port = random.randint(1, 65535)
            packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port)
        elif protocol == 'UDP':
            src_port = random.randint(1024, 65535)
            dst_port = random.randint(1, 65535)
            packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port)
        
        packets.append(packet)
    
    return packets

# Define the destination IP addresses
destinations = ["192.16.1.{}".format(i) for i in range(2, 9)]  # 7 different destinations

# Number of packets to start with
initial_num_packets = 10
# Number of packets to add in each iteration
increment_num_packets = 20

# Main loop to send packets
packets = generate_packets(initial_num_packets, destinations)

while True:
    # Send packets
    send(packets, verbose=False)
    print(f"Sent {len(packets)} packets")
    
    # Add more packets for the next round
    packets += generate_packets(increment_num_packets, destinations)
    
    # Wait for 10 to 15 seconds before sending the next batch
    wait_time = random.randint(10, 15)
    print(f"Waiting for {wait_time} seconds before the next batch")
    time.sleep(wait_time)
