import pytest
import requests

class TestAPIEndpoints:
    def test_run_task_success(self, server_setup):
        url = f"{server_setup}/run_task"
        data = {"task_name": "dns_query", "params": {"domain": "example.com"}}
        response = requests.post(url, json=data)

        assert response.status_code == 200
        result = response.json()
        assert result["domain"] == "example.com"
        assert "ip_address" in result

    def test_run_task_missing_task_name(self, server_setup):
        url = f"{server_setup}/run_task"
        data = {"params": {"domain": "example.com"}}
        response = requests.post(url, json=data)

        assert response.status_code == 400
        result = response.json()
        assert result["status"] == "error"
        assert "Task name is required" in result["message"]

    def test_run_tasks_parallel_execution(self, server_setup):
        url = f"{server_setup}/run_tasks"
        data = {
            "tasks": [
                {"task_name": "dns_query", "params": {"domain": "example.com"}},
                {"task_name": "http_get_request",  "params": {"domain_or_ip":"www.dlptest.com","port":443,"uri":"/login"}}
            ]
        }
        response = requests.post(url, json=data)

        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert len(result["results"]) == 2

    def test_run_tasks_no_tasks(self, server_setup):
        url = f"{server_setup}/run_tasks"
        data = {"tasks": []}
        response = requests.post(url, json=data)

        assert response.status_code == 400
        result = response.json()
        assert result["status"] == "error"
        assert "No tasks provided" in result["message"]


