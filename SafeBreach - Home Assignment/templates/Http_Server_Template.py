import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import uuid4

class HTTPServerTemplate:
    def __init__(self):
        # ========================
        # Server Initialization
        # ========================
        # Dictionary to store active server details
        self.active_servers = {}
        # Maximum number of servers allowed to run concurrently
        self.max_servers = 10
        # Lock to ensure thread-safe operations
        self.lock = threading.Lock()


    def start_http_server(self, port, page_uri, response_data):
        """
        Starts an HTTP server on a specified port, serving a specified URI with a response.
        """
        with self.lock:
            # Check if the maximum number of servers is reached
            if len(self.active_servers) >= self.max_servers:
                return {"status": "error", "message": f"Cannot create more than {self.max_servers} servers"}

            # Validate port range
            if port < 1024 or port > 65535:
                return {"status": "error", "message": "Port must be between 1024 and 65535"}

            # Check if the port is already in use
            for server_id, details in self.active_servers.items():
                if details["port"] == port:
                    return {
                        "status": "error",
                        "message": f"Port {port} is already in use by server {server_id}"
                    }

            # Generate a unique ID for the new server
            server_id = str(uuid4())

            # Define the request handler class
            class RequestHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == page_uri:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(response_data.encode())
                    else:
                        self.send_response(404)
                        self.end_headers()

            def run_server():
                """
                Run the HTTP server on the specified port.
                """
                try:
                    server = HTTPServer(("0.0.0.0", port), RequestHandler)
                    # Add server details to the active servers list
                    with self.lock:
                        self.active_servers[server_id] = {
                            "port": port,
                            "page_uri": page_uri,
                            "server": server,
                        }
                    server.serve_forever()
                except Exception as e:
                    # Remove the server from the active list if an error occurs
                    with self.lock:
                        if server_id in self.active_servers:
                            del self.active_servers[server_id]

            try:
                # Start the server in a new thread
                server_thread = threading.Thread(target=run_server, daemon=True)
                server_thread.start()
                return {"status": "success", "server_id": server_id, "port": port}
            except Exception as e:
                return {"status": "error", "message": str(e)}


    def stop_http_server(self, server_id):
        """
        Stops a running HTTP server identified by its server ID.
        """
        with self.lock:
            if server_id in self.active_servers:
                # Shutdown the server and remove it from the active list
                server = self.active_servers[server_id]["server"]
                server.shutdown()
                del self.active_servers[server_id]
                return {"status": "success", "message": f"Server {server_id} stopped"}
            return {"status": "error", "message": "Server ID not found"}

    def list_active_servers(self):
        """
        Returns a list of all currently active servers.
        """
        with self.lock:
            return [
                {"server_id": server_id, "port": details["port"], "page_uri": details["page_uri"]}
                for server_id, details in self.active_servers.items()
            ]
