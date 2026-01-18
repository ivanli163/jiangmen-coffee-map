import http.server
import socketserver
import socket

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    pass

# Ensure we bind to IPv4
class TCPServer(socketserver.TCPServer):
    address_family = socket.AF_INET

with TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}")
    print(f"Try accessing via http://192.168.3.29:{PORT}")
    httpd.serve_forever()
