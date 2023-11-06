import json
from unittest.mock import patch
import pytest
import flask
from app import add_task, app, by_category, categories, delete_task, find_task_by_id, get_all_tasks, get_task, mark_complete, update

task_list = [{"id": 1, "description": "test task one", "category": "test", "status": "pending"}, 
    {"id": 2, "description": "test task two", "category": "test", "status": "pending"}, 
    {"id": 3, "description": "test task three", "category": "test_again", "status": "complete"}]

def mock_save_tasks(tasks):
    task_list = tasks

@pytest.fixture
def mock_task_list(mocker):
    mocker.patch("app.get_tasks", return_value=task_list)
    mocker.patch("app.save_tasks", return_value=mock_save_tasks)

def test_find_task_by_id(mock_task_list):
    assert find_task_by_id(2) == task_list[1]

def test_get_all_tasks(mock_task_list):
    with app.test_request_context("/tasks", method="GET"):
        response = get_all_tasks()
        print(response)
    assert "test task one" in response[0]

def test_add_task(mock_task_list):
    with app.test_request_context("/tasks", 
        method="POST", 
        content_type="application/json",
        data=json.dumps({"id": 4, "description": "test task four", "category": "test_add_task"})):

        response = add_task()
    assert response[1] == 201

def test_get_task(mock_task_list):
    with app.test_client() as c:
        response = c.get("/tasks/3").json
        assert response["description"] == "test task three"

def test_delete_task(mock_task_list):
    with app.test_client() as c:
        response = c.delete("/tasks/2").json
        print(response)
    assert response["message"] == "Autentisering misslyckades."

def test_update(mock_task_list):
    with app.test_client("/tasks/1", method="PUT", 
            content_type="application/json",
            data=json.dumps({"id": 1, "description": "test task one", "category": "test_update_task"})):
        response = update(1).get_json()
    assert "test_update_task" in response

def test_mark_complete(mock_task_list):
    with app.test_request_context("/tasks/1/complete", method="PUT"):
        response = mark_complete(1).get_json()
    assert "completed" in response

def test_categories(mock_task_list):
    with app.test_request_context("/tasks/categories", method="GET"):
        response = categories().get_json()
    assert "test" in response

def test_by_category(mock_task_list):
    with app.test_request_context("/tasks/categories/test_again", method="GET"):
        response = by_category("test").get_json()
        print(task_list)
        print(json.loads(response))
    assert len(json.loads(response)) == 1



"""