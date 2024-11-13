import socket

# Define the port to listen on
PORT = 8082

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to the port
    s.bind(('', PORT))
    print("Listening for broadcast messages...")

    while True:
        # Receive data and address from the sender
        data, addr = s.recvfrom(1024)
        print(f"Received broadcast message from {addr[0]}: {data.decode()}")

        # Send a response back to the sender
        response_message = "Hello from the other device!"
        s.sendto(response_message.encode(), addr)
        print("Response sent.")
