import socket
import time

# Define broadcast address and port
BROADCAST_ADDRESS = 'localhost'  # Broadcast address192.168.198.255
PORT = 8082

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Enable broadcasting
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send broadcast message
    message = "Hi"
    s.sendto(message.encode(), (BROADCAST_ADDRESS, PORT))
    print("Broadcast message sent.")

    # Receive responses
    round_trip_times = {}
    start_time = time.time()
    serial_number = 1
    while True:
        # Set a timeout for receiving response
        s.settimeout(2.0)  # Timeout of 2 seconds
        
        try:
            # Receive data from any device
            data, addr = s.recvfrom(1024)
            round_trip_time = time.time() - start_time
            if addr[0] != BROADCAST_ADDRESS:  # Exclude the broadcast sender itself
                if addr[0] not in round_trip_times:
                    round_trip_times[addr[0]] = round_trip_time
                print(f"Received from {addr[0]}: {data.decode()} (Round Trip Time: {round_trip_time:.6f} seconds)")
                serial_number += 1
        except socket.timeout:
            print("No more responses.")
            break

print("Broadcast round trip times:")
for device, rt_time in round_trip_times.items():
    print("Device:", device, "Round Trip Time:", rt_time)

# Find the device with the shortest round-trip time
shortest_rtt_device = None
shortest_rtt = float('inf')

for device, rt_time in round_trip_times.items():
    if rt_time < shortest_rtt:
        shortest_rtt = rt_time
        shortest_rtt_device = device

if shortest_rtt_device:
    print(f"Device with the shortest RTT: {shortest_rtt_device} (RTT: {shortest_rtt:.6f} seconds)")
else:
    print("No devices responded.")

'''
import socket
import time

# Define broadcast address and port
BROADCAST_ADDRESS = '192.168.198.255'#'broadcast'192.168.224.255
PORT = 8081

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Enable broadcasting
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send broadcast message
    message = "Hi"
    s.sendto(message.encode(), (BROADCAST_ADDRESS, PORT))
    print("Broadcast message sent.")

    # Receive responses
    round_trip_times = {}
    start_time = time.time()
    serial_number = 1
    while True:
        # Set a timeout for receiving response
        s.settimeout(2.0)  # Timeout of 2 seconds
        
        try:
            # Receive data from any device
            data, addr = s.recvfrom(1024)
            round_trip_time = time.time() - start_time
            if addr[0] not in round_trip_times:
                round_trip_times[addr[0]] = []
            round_trip_times[addr[0]].append((serial_number, round_trip_time))
            print(f"Received from {addr[0]}: {data.decode()} (Round Trip Time: {round_trip_time:.6f} seconds)")
            serial_number += 1
        except socket.timeout:
            print("No more responses.")
            break

print("Broadcast round trip times:")
for device, times in round_trip_times.items():
    print("Device:", device)
    for serial_number, rt_time in times:
        print("Serial Number:", serial_number, "Round Trip Time:", rt_time)
'''
