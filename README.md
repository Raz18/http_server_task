# Overview

This project is a modular Python-based task management framework featuring:

A Flask API server to interact with clients.

A backend task executor.

A custom HTTP server creation template.

The system supports:
DNS queries.
HTTP GET requests.
Dynamic creation of HTTP servers.
It is extendable, supports parallel task execution, and ensures efficient HTTP servers creation and management, all from a single API server as requested!.

## Project Structure

**1. Main API Task Initiator Server (Main_API_Initiator.py)**
This file acts as the entry point for the system and implements a Flask-based REST API.

Key Functionalities of the Endpoints:

/run_task: Executes a single task based on the provided task name and parameters (e.g., dns_query, http_get, create_http_server_task).

/run_tasks: Executes multiple tasks in parallel and returns results for all.

/active_servers: Lists all currently active HTTP servers, including their server_id, port, and page_uri.

/stop_server: Stops an active server by specifying the server_id.

**Task Execution Flow**
  
The Flask server routes incoming API requests to the backend API tasks for processing.

Tasks are executed based on the task name and parameters.

Example Usage

```bash
POST /run_task
Content-Type: application/json
{
  "task_name": "dns_query",
  "params": {
    "domain": "example.com"
  }
}
```
```bash
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
        "page_uri": "/test", 
        "response_data": "This is a test page!" 
      }
    }
  ]
}


```

**2. API Tasks File (Server_Tasks.py)**

This module implements the backend logic for executing tasks the tasks. 

**Features**

Centralized task execution logic for scalability.

Extendable to add new tasks by modifying the Main API class.

Validates inputs for robust error handling,


**3. HTTP Server Template (Http_Server_Template.py)**

This module provides the logic for creating and managing HTTP servers using Python's HTTPServer.

**Key Functionalities**

Create New HTTP Servers

Dynamically starts a new server on the specified port and URI.

Tracks each server with a unique server_id.

Track Active Servers.

Maintains a dictionary of active servers (port, URI, server thread).

Prevents duplication of servers on the same port or URI.

Ensures a maximum of 10 servers are active.

Validates port and URI availability before starting a new server.

Safely shuts down servers when requested.


## Running the Framework

```python
#Dependencies
pip install flask requests pytest

# starting the main server to receive tasks
python Main_API_Initiator


url = "http://127.0.0.1:5000/run_task"
#domain query task
payload = {
    "task_name": "dns_query",
    "params": {
        "domain": "example.com"
    }
}
response = requests.post(url, json=payload)
print(response.json())


#http get task
payload = {
    "task_name": "http_get_request",
    "params": {
        "domain_or_ip": "example.com",
        "port": 443,
        "uri": "/"
    }
}
response = requests.post(url, json=payload)
print(response.json())

#create http server task

payload = {
    "task_name": "start_http_server",
    "params": {
        "port": 50010,
        "page_uri": "/test",
        "response_data": "This is a test page!"
    }
}
response = requests.post(url, json=payload)
print(response.json())

```

## Testing the Framework

Unit tests are implemented using pytest to validate all supported tasks functionalities and overall task execution flow, it includes a conftest file and for a centralized setup and variable management.

Run the tests from the App_tests directory:
```bash
pytest App_tests/
```
