import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

# Constants
BROADCAST_PORT = 8082  # Broadcast listening port
HTTP_PORT = 8081  # HTTP server port
BROADCAST_ADDRESS = '192.168.224.225'  # Change to the actual broadcast address

# Define the request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Construct the full URL
        full_url = f"http://{self.headers['Host']}{self.path}"
        
        # Store the full URL in a local variable and print it
        self.received_url = full_url
        print(f"Received request for URL: {self.received_url}")

        # Extract the IP address from the URL
        received_ip = self.headers['Host'].split(':')[0]

        # Run the broadcast function
        run_broadcast(received_ip, self.received_url)

def run_broadcast(exclude_ip, received_url):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Enable broadcasting
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Send broadcast message
        message = "Hi"
        s.sendto(message.encode(), (BROADCAST_ADDRESS, BROADCAST_PORT))
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
                if addr[0] != BROADCAST_ADDRESS and addr[0] != exclude_ip:  # Exclude the broadcast sender itself and the received IP
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
        
        # Replace the IP in the received URL and send the new URL
        new_url = received_url.replace(exclude_ip, shortest_rtt_device)
        print(f"Sending new URL: {new_url}")
        requests.get(new_url)
        try:
            
            # Send HTTP GET request
            response = requests.get(new_url)
            if response.status_code == 200:
                print("Data sent successfully.")
            else:
                print("Failed to send data. Response code:", response.status_code)
        except requests.exceptions.ConnectionError as e:
            print("Connection error:", e)
    else:
        print("No devices responded.")

def run_http_server():
    # Custom server class to pass the broadcast socket
    class CustomHTTPServer(HTTPServer):
        def __init__(self, server_address, RequestHandlerClass):
            super().__init__(server_address, RequestHandlerClass)

    server_address = ('', HTTP_PORT)
    httpd = CustomHTTPServer(server_address, RequestHandler)
    print("Starting server on port 8081...")
    httpd.serve_forever()

def handle_broadcast():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket:
        # Bind the socket to the broadcast port
        broadcast_socket.bind(('', BROADCAST_PORT))
        print("Listening for broadcast messages...")

        while True:
            # Receive data and address from the sender
            data, addr = broadcast_socket.recvfrom(1024)
            print(f"Received broadcast message from {addr[0]}: {data.decode()}")

            # Send a response back to the sender
            response_message = "Hello from the other device!"
            broadcast_socket.sendto(response_message.encode(), addr)
            print("Response sent.")

if __name__ == '__main__':
    # Start broadcast handler in a separate thread
    broadcast_thread = threading.Thread(target=handle_broadcast)
    broadcast_thread.start()

    # Start HTTP server
    run_http_server()
