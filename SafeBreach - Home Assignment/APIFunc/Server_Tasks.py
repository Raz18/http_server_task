import socket
import requests

from templates.Http_Server_Template import HTTPServerTemplate
from utils.logger import LoggerConfig


class APIEndpoints:
    # Initialize logger and HTTP server task manager
    logger = LoggerConfig.get_logger("APIEndpoints")
    http_server_task = HTTPServerTemplate()

    @staticmethod
    def execute_task(task_name, params):
        """
        task execution list based on task_name.
        Maps task names to corresponding methods and executes them with given parameters.
        """
        tasks = {
            "dns_query": APIEndpoints.dns_query,
            "http_get_request": APIEndpoints.http_get_request,
            "start_http_server": APIEndpoints.start_http_server,
            "list_http_active_servers": APIEndpoints.list_http_active_servers,
            "stop_http_active_server": APIEndpoints.stop_http_active_server,
        }
        try:
            if task_name in tasks:
                APIEndpoints.logger.info(f"Task {task_name} completed successfully.")
                return tasks[task_name](**params)
        except Exception as e:
            return {"status": "error", "message": "{}, please try again".format(e)}
    @staticmethod
    def dns_query(domain):
        """
        Resolves a domain to an IP address.
        """
        if not domain:
            return {"status": "error", "message": "Please enter a valid domain"}
        try:
            ip_address = socket.gethostbyname(domain)
            return {"domain": domain, "ip_address": ip_address}
        except socket.gaierror as e:
            return {"error": f"Failed to resolve domain: {str(e)}"}


    @staticmethod
    def http_get_request(domain_or_ip, port=None, uri=""):
        """
        Performs an HTTP GET request.
        Defaults to https on port 443 unless port 80 or a port starting with 80 is provided.
        """
        # Default to port 443 and https
        if port is None:
            port = 443

        if str(port).startswith("80"):
            protocol = "http"
        else:
            protocol = "https"

        url = f"{protocol}://{domain_or_ip}:{port}{uri}"
        try:
            response = requests.get(url)
            return {
                "url": url,
                "status_code": response.status_code,
                "data": response.text
            }
        except requests.RequestException as e:
            return {"error": f"HTTP GET request failed: {str(e)}"}


    # Start HTTP Server
    @staticmethod
    def start_http_server(port, page_uri, response_data):
        """
        Starts a new HTTP server using HTTPServerTask Class Template.
        """
        return APIEndpoints.http_server_task.start_http_server(port, page_uri, response_data)

    # List Active HTTP Servers
    @staticmethod
    def list_http_active_servers():
        """
        Lists all currently active HTTP servers.
        """
        return APIEndpoints.http_server_task.list_active_servers()

    # Stop HTTP Server
    @staticmethod
    def stop_http_active_server(server_id):
        """
        Stops an active HTTP server by its server_id.
        """
        return APIEndpoints.http_server_task.stop_http_server(server_id)
