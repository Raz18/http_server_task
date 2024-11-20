import pytest
import subprocess
import requests
import time

@pytest.fixture(scope="session")
def server_setup(request):
    """
    Fixture to start and stop the Flask server for testing.
    Dynamically determines the port to open the API.
    """
    port = request.config.getoption("--port") or "5000"
    server_url = f"http://127.0.0.1:{port}"

    # Start the server in a subprocess
    process = subprocess.Popen(
        ["python", "Main_API_Initiator.py"],  # Replace `app.py` with your main server file
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"FLASK_RUN_PORT": port},
    )
    time.sleep(2)  # Wait for the server to start

    # Check if the server is reachable
    try:
        response = requests.get(server_url)
        if response.status_code != 404:  # Assuming 404 is expected for root
            raise Exception("Server did not start correctly")
    except Exception as e:
        process.terminate()
        raise RuntimeError(f"Server failed to start: {e}")

    # Yield the server URL for the tests
    yield server_url

    # Teardown
    process.terminate()
    process.wait()

def pytest_addoption(parser):
    """
    Add custom CLI options to pytest.
    """
    parser.addoption(
        "--port", action="store", default="5000", help="Port to run the server on"
    )
