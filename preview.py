import http.server
import socketserver
import webbrowser
import os
from build import build_site

PORT = 8000

def run_server():
    # Change into the directory where this script is, to ensure we serve the right files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Build the site before starting
    print("Building site...")
    build_site()
    
    # Allow address reuse in case of recent restart
    socketserver.TCPServer.allow_reuse_address = True
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Opening browser...")
        webbrowser.open(f"http://localhost:{PORT}/index.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
