import socket
import time

# Define broadcast address and port
BROADCAST_ADDRESS = '192.168.198.255'
PORT = 8081

# Create a socket object for broadcasting
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Create a socket object for listening
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen_socket.bind(('', PORT))
print("Listening for broadcast messages...")

# Dictionary to store round-trip times for connected devices
round_trip_times = {}

while True:
    # Send broadcast message
    message = "Hi"
    broadcast_socket.sendto(message.encode(), (BROADCAST_ADDRESS, PORT))
    print("Broadcast message sent.")

    # Receive responses
    start_time = time.time()
    while True:
        # Set a timeout for receiving response
        listen_socket.settimeout(1.0)  # Timeout of 2 seconds , changed to 1
        
        try:
            # Receive data from any device
            data, addr = listen_socket.recvfrom(1024)
            round_trip_time = time.time() - start_time
            if addr[0] != BROADCAST_ADDRESS:  # Exclude the sender itself
                if addr[0] not in round_trip_times:
                    round_trip_times[addr[0]] = []
                round_trip_times[addr[0]].append(round_trip_time)
                print(f"Received from {addr[0]}: {data.decode()} (Round Trip Time: {round_trip_time:.6f} seconds)")
            else:
                print("Response from sender, excluding from RTT calculation.")
        except socket.timeout:
            print("No more responses.")
            break

    print("Broadcast round trip times:")
    for device, times in round_trip_times.items():
        print("Device:", device)
        for rt_time in times:
            print("Round Trip Time:", rt_time)

    # Find the device with the shortest round-trip time
    shortest_rtt_device = min(round_trip_times, key=lambda x: sum(round_trip_times[x]) / len(round_trip_times[x]))
    print("Shortest RTT device:", shortest_rtt_device)

    # Forward the URL to the device with the shortest round-trip time
    if shortest_rtt_device:
        # Construct the new URL with the IP address of the device with shortest RTT
        new_url = "http://" + shortest_rtt_device + ":8081/insertTemperature"

        # Replace the placeholder in the received URL with the new IP address
        received_url = data.decode()
        new_url = received_url.replace("INSERT_IP_HERE", shortest_rtt_device)

        try:
            response = requests.get(new_url)
            if response.status_code == 200:
                print("URL forwarded successfully to:", shortest_rtt_device)
            else:
                print("Failed to forward URL to:", shortest_rtt_device)
        except requests.RequestException as e:
            print("Error forwarding URL to", shortest_rtt_device, ":", e)
            print("Forwarding URL:", new_url)

# Close the sockets
broadcast_socket.close()
listen_socket.close()
