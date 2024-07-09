import libnet

# Create a libnet context
l = libnet.context()

# Build and send the first packet
packet_1 = IP(dst="10.0.0.2")/UDP(dport=1234)/Raw(load="packet 1")
l.injection_rate = 1
l.repeat = 1
l.interpacket_time = 1
l.bytecount = len(packet_1)
l.build_ipv4()
l.build_udp()
l.write(packet_1.build())

# Build and send the second packet
packet_2 = IP(dst="10.0.0.2")/TCP(dport=5678)/Raw(load="packet 2")
l.bytecount = len(packet_2)
l.build_ipv4()
l.build_tcp()
l.write(packet_2.build())

# Build and send the third packet
packet_3 = IP(dst="10.0.0.2")/ICMP()/Raw(load="packet 3")
l.bytecount = len(packet_3)
l.build_ipv4()
l.build_icmp()
l.write(packet_3.build())

