HTTP Server Task Management Framework
Overview
This project is a modular Python-based task management framework featuring:

A Flask API server to interact with clients.
A backend task executor.
A custom HTTP server manager.
The system supports:

DNS queries.
HTTP GET requests.
Dynamic creation of HTTP servers.
It is extendable, supports parallel task execution, and ensures efficient HTTP server management.

Project Structure
1. Main API Task Initiator Server (main_api.py)
This file acts as the entry point for the system and implements a Flask-based REST API.

Key Functionalities:
Endpoints:
/run_task: Executes a single task based on the provided task name and parameters (e.g., dns_query, http_get, create_http_server_task).
/run_tasks: Executes multiple tasks in parallel and returns results for all.
/active_servers: Lists all currently active HTTP servers, including their server_id, port, and page_uri.
/stop_server: Stops an active server by specifying the server_id.
Task Execution Flow
The Flask server routes incoming API requests to the backend API tasks for processing.
Tasks are executed based on task name and parameters.
Features:
Input validation for API requests.
Proper error handling with meaningful responses.
Concurrent task execution using a thread pool.
Example Usage
Run a Task:
http
Copy code
POST /run_task
Content-Type: application/json
{
  "task_name": "dns_query",
  "params": {
    "domain": "example.com"
  }
}
Run Multiple Tasks:
http
Copy code
POST /run_tasks
Content-Type: application/json
{
  "tasks": [
    {
      "task_name": "dns_query",
      "params": { "domain": "example.com" }
    },
    {
      "task_name": "http_get_request",
      "params": { 
        "domain_or_ip": "example.com", 
        "port": 443, 
        "uri": "/" 
      }
    },
    {
      "task_name": "create_http_server",
      "params": { 
        "port": 50010, 
        "page_uri": "/rssss", 
        "response_data": "This is a test page!" 
      }
    }
  ]
}
2. API Tasks File (Server_Tasks.py)
This module implements the backend logic for executing tasks.

Supported Tasks:
DNS Query: Resolves a domain name to its IP address.
HTTP GET Request: Sends an HTTP GET request to a specified domain/IP with support for HTTPS (default for port 443).
Start HTTP Server: Dynamically creates an HTTP server with predefined content.
List Active HTTP Servers: Provides a list of all active servers with details like port, URI, and server_id.
Stop Active HTTP Server: Stops a running server by its server_id.
Features:
Centralized task execution logic for scalability.
Extendable to add new tasks by modifying the TaskInitiator class.
Validates inputs for robust error handling.
3. HTTP Server Template (Http_Server_Template.py)
This module provides the logic for creating and managing HTTP servers using Python's HTTPServer.

Key Functionalities:
Create New HTTP Servers:
Dynamically starts a new server on the specified port and URI.
Tracks each server with a unique server_id.
Track Active Servers:
Maintains a dictionary of active servers (port, URI, server thread).
Prevents duplication of servers on the same port or URI.
Validation:
Ensures a maximum of 10 servers are active.
Validates port and URI availability before starting a new server.
Proper Shutdown:
Safely shuts down servers when requested.
Running the Framework
Install Dependencies
Ensure Python is installed and use the following command to install required packages:

bash
Copy code
pip install flask requests pytest
Start the Main API Server
Run the main API server to expose its endpoints:

bash
Copy code
python main_api.py
Interact with the API
Use tools like Postman or Python’s requests library to send requests to the server.

Testing the Framework
Unit tests are implemented using pytest to validate functionalities and task execution flow.

Run Tests
Run the tests from the App_tests directory:

bash
Copy code
pytest App_tests/
Extending the Framework
Add New Tasks
Define a new method in the Server_Tasks class with the logic for the task.
Update the execute_task method to route to the new task.
Add New Endpoints
Add new routes to the main_api.py file.
Ensure proper mapping between the route and task logic.
Key Highlights
Modular, extensible architecture.
Robust validation and error handling.
Supports concurrent execution of tasks.
Easy integration with external tools and APIs.
