from flask import request, jsonify, redirect, Flask
from concurrent.futures import as_completed, ThreadPoolExecutor
from APIFunc.Server_Tasks import APIEndpoints

# Flask app initialization
app = Flask(__name__)

# Global thread pool for parallel task execution
executor = ThreadPoolExecutor()

class TaskInitiator:
    @staticmethod
    @app.route('/run_task', methods=['POST'])
    def run_task():
        """
        API endpoint to run a single task.
        Handles POST requests to execute a task based on its name and parameters.
        """
        if request.method == 'GET':
            return 'Not Allowed'

        data = request.json
        task_name = data.get("task_name")
        params = data.get("params", {})

        if not task_name:
            return jsonify({"status": "error", "message": "Task name is required"}), 400

        result = APIEndpoints.execute_task(task_name, params)
        return jsonify(result)

    @staticmethod
    @app.route('/run_tasks', methods=['POST'])
    def run_tasks():
        """
        API endpoint to run multiple tasks in parallel.
        Accepts a list of tasks with task names and parameters, and executes them concurrently.
        """
        data = request.json
        tasks = data.get("tasks", [])

        if not tasks:
            return jsonify({"status": "error", "message": "No tasks provided"}), 400

        # Submit tasks to the thread pool
        futures = [
            executor.submit(APIEndpoints.execute_task, task.get("task_name"), task.get("params", {}))
            for task in tasks
        ]

        # Collect results as they complete
        results = [future.result() for future in as_completed(futures)]

        return jsonify({"status": "success", "results": results})

    @staticmethod
    @app.route('/active_servers', methods=['GET'])
    def active_servers():
        """
        API endpoint to list all active HTTP servers.
        Queries the APIEndpoints class for currently active HTTP servers and their details.
        """
        servers = APIEndpoints.list_http_active_servers()
        return jsonify({"status": "success", "active_servers": servers})

    @staticmethod
    @app.route('/stop_server', methods=['POST'])
    def stop_server():
        """
        API endpoint to stop an active HTTP server.
        Requires a server_id to identify the server to stop.
        """
        data = request.json  # Get the JSON data from the request
        server_id = data.get("server_id")  # Extract the server_id from the request

        if not server_id:
            return jsonify({"status": "error", "message": "Server ID is required"}), 400

        # Call the stop_http_active_server method
        result = APIEndpoints.stop_http_active_server(server_id)

        # Return the result as a JSON response
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
