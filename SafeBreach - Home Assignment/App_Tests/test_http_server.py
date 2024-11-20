from time import sleep

import pytest
import requests

class TestHTTPServerManagement:
    def test_start_http_server(self, server_setup):
        url = f"{server_setup}/run_task"
        print(url)
        data = {
            "task_name": "start_http_server",
            "params": {"port": 55555, "page_uri": "/test", "response_data": "Hello, World!"}
        }
        response = requests.post(url, json=data)
        sleep(3)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success", "failed creating server"
        assert "server_id" in result, "failed creating server"

        first_server_id= result["server_id"]
        #print(first_server_id)
        # Test the running HTTP server
        server_url = f"http://127.0.0.1:55555/test"
        server_response = requests.get(server_url)

        assert server_response.status_code == 200, "failed reaching created server"

        assert server_response.text == "Hello, World!", "failed reaching created server"
        #print(server_response.text)

    def test_list_active_servers(self, server_setup):
        url = f"{server_setup}/active_servers"
        response = requests.get(url)
        assert response.status_code == 200
        result = response.json()
        #print(result)
        assert isinstance(result["active_servers"], list)
        assert len(result["active_servers"]) > 0

    def test_stop_http_server(self, server_setup):
        url = f"{server_setup}/run_task"
        #print(url)
        data = {
            "task_name": "start_http_server",
            "params": {"port": 35674, "page_uri": "/test", "response_data": "Hello, World!"}
        }
        response = requests.post(url, json=data)
        sleep(5)
        assert response.status_code == 200
        result = response.json()
        print(result["server_id"])
        # Stop the server
        stop_url = f"{server_setup}/stop_server"
        stop_data = {"server_id": result["server_id"] }
        #print(stop_data)
        stop_response = requests.post(stop_url, json=stop_data)
        sleep(3)
        stop_result = stop_response.json()
        assert stop_response.status_code == 200
        print(stop_result)
        assert result["status"] == "success", "failed stopping server"+ result["message"]

    def test_start_http_server_invalid_port(self, server_setup):
        """
        Test starting an HTTP server with an invalid port.
        """
        url = f"{server_setup}/run_task"

        # Port below 1024
        data_low_port = {
            "task_name": "start_http_server",
            "params": {"port": 500, "page_uri": "/test", "response_data": "Invalid Port"}
        }
        response_low_port = requests.post(url, json=data_low_port)
        assert response_low_port.status_code == 200
        result_low_port = response_low_port.json()
        assert result_low_port["status"] == "error"
        assert "Port must be between 1024 and 65535" in result_low_port["message"]

        # Port above 65535
        data_high_port = {
            "task_name": "start_http_server",
            "params": {"port": 777777, "page_uri": "/test", "response_data": "Invalid Port"}
        }
        response_high_port = requests.post(url, json=data_high_port)
        assert response_high_port.status_code == 200
        result_high_port = response_high_port.json()
        assert result_high_port["status"] == "error"
        assert "Port must be between 1024 and 65535" in result_high_port["message"]

    def test_max_servers(self, server_setup):
        """
        Test starting the maximum number of HTTP servers (10) and ensure the 11th attempt fails.
        """
        url = f"{server_setup}/run_task"
        active_servers = []

        # Start the maximum number of servers (10)
        for i in range(11):
            data = {
                "task_name": "start_http_server",
                "params": {"port": 8000 + i, "page_uri": f"/test{i}", "response_data": f'test{i}'}
            }
            response = requests.post(url, json=data)
            sleep(3)
            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "success"
            assert "server_id" in result
            active_servers.append(result["server_id"])


        # Attempt to start an 11th server
        data_11th = {
            "task_name": "start_http_server",
            "params": {"port": 8010, "page_uri": "/test11", "response_data": "Server 11"}
        }
        response_11th = requests.post(url, json=data_11th)
        assert response_11th.status_code == 200
        result_11th = response_11th.json()
        assert result_11th["status"] == "error"
        assert "Cannot create more than 10 servers" in result_11th["message"]
        #print(active_servers)
        #servers cleanup at the end of the test
        for server_id in active_servers:
            stop_url = f"{server_setup}/stop_server"
            requests.post(stop_url, json={"server_id": server_id})
            sleep(3)
