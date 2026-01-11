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
    
    # Define Handler
    Handler = http.server.SimpleHTTPRequestHandler

    # Find a free port
    port = PORT
    while True:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                print(f"Serving at http://localhost:{port}")
                print("Opening browser...")
                webbrowser.open(f"http://localhost:{port}/index.html")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nServer stopped.")
                break
        except OSError:
            print(f"Port {port} is in use, trying {port + 1}...")
            port += 1
            if port > 8100:
                print("Could not find a free port.")
                break
        print(f"Serving at http://localhost:{PORT}")
        print("Opening browser...")
        webbrowser.open(f"http://localhost:{PORT}/index.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
