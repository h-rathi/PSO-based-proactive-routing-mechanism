
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define the request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Construct the full URL
        full_url = f"http://{self.headers['Host']}{self.path}"
        
        # Store the full URL in a local variable and print it
        self.received_url = full_url
        print(f"Received request for URL: {self.received_url}")

        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Write content as utf-8 data
        self.wfile.write(bytes("Data received successfully.", "utf8"))

        #send broadcast
        
        

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
from http.server import BaseHTTPRequestHandler, HTTPServer
'''
# Define the request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Construct the full URL
        full_url = f"http://{self.headers['Host']}{self.path}"
        
        # Store the full URL in a local variable and print it
        self.received_url = full_url
        print(f"Received request for URL: {self.received_url}")

        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Write content as utf-8 data
        self.wfile.write(bytes("Data received successfully.", "utf8"))
        

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()



from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# Define the request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Construct the full URL
        full_url = f"http://{self.headers['Host']}{self.path}"
        
        # Log the full URL that was accessed
        logging.info(f"Received request for URL: {full_url}")
        print(f"Received request for URL: {full_url}")

        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Write content as utf-8 data
        self.wfile.write(bytes("Data received successfully.", "utf8"))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    logging.info(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
'''
