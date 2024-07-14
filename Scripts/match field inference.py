from scapy.all import send, sr1, IP, TCP, Ether, ICMP
import random
import time

# Function to generate a random IP address
def random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Function to send packets with varying match fields and calculate RTT
def send_packets(num_packets=10):
    rtt_list = []
    
    for i in range(num_packets):
        src_ip = random_ip()
        dst_ip = random_ip()
        src_port = random.randint(1024, 65535)
        dst_port = random.randint(1024, 65535)

        # Create packet with varying match fields
        packet = IP(src=src_ip, dst=dst_ip) / ICMP()
        
        print(f"Sending packet {i+1}/{num_packets}: {src_ip} -> {dst_ip}")
        
        # Send the packet and measure RTT
        start_time = time.time()
        response = sr1(packet, timeout=1, verbose=0)
        end_time = time.time()
        
        if response:
            rtt = (end_time - start_time) * 1000  # Convert to milliseconds
            rtt_list.append(rtt)
            print(f"RTT: {rtt:.2f} ms")
        else:
            print("No response")
    
    return rtt_list

if __name__ == "__main__":
    num_packets = 10  # Number of packets to send
    rtt_list = send_packets(num_packets)
    
    # Print RTT list
    print("\nRTT List (ms):")
    for idx, rtt in enumerate(rtt_list, start=1):
        print(f"{idx}: {rtt:.2f} ms")

