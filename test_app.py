import json
import pytest
from app import app, find_task_by_id

task_list = [{"id": 1, "description": "test task one", "category": "test", "status": "pending"}, 
    {"id": 2, "description": "test task two", "category": "test", "status": "pending"}, 
    {"id": 3, "description": "test task three", "category": "test_again", "status": "completed"}]

def mock_save_tasks(tasks):
    task_list = tasks

@pytest.fixture
def mock_task_list(mocker):
    mocker.patch("app.get_tasks", return_value=task_list)
    mocker.patch("app.save_tasks", return_value=mock_save_tasks)

def test_find_task_by_id(mock_task_list):
    assert find_task_by_id(2) == task_list[1]

def test_get_all_tasks(mock_task_list):
    with app.test_client() as c:
        response = c.get("/tasks").json
    assert response[0]["description"] == "test task one"

def test_add_task(mock_task_list):
    assert len(task_list) == 3
    with app.test_client() as c:
        add_data=json.dumps({"id": 4, "description": "test task four", "category": "test_add_task"})
        response = c.post("/tasks", data=add_data, content_type="application/json").status_code
    assert response == 201
    assert len(task_list) == 4

def test_get_task(mock_task_list):
    with app.test_client() as c:
        response = c.get("/tasks/3").json
    assert response["description"] == "test task three"

def test_delete_task_no_auth(mock_task_list):
    with app.test_client() as c:
        response = c.delete("/tasks/2")
    assert "Autentisering misslyckades." == response.json["message"]
    assert 401 == response.status_code

def test_delete_task_correct_auth(mock_task_list):
    with app.test_client() as c:
        response = c.delete("/tasks/2", headers={"Authorization": "Bearer my_secret_token"})
    assert "Uppgiften har tagits bort." == response.json["message"]
    assert 202 == response.status_code
    assert len(task_list) == 3


def test_update(mock_task_list):
    with app.test_client() as c:
        update_data=json.dumps({"id": 1, "description": "test task one", "category": "test_update_task"})
        response = c.put("/tasks/1", data=update_data, content_type="application/json").json
        print(response)
    assert response["category"] == "test_update_task"

def test_mark_complete(mock_task_list):
    with app.test_client() as c:
        response = c.put("/tasks/1/complete").json
    assert "avslutad" in response["message"]
    assert task_list[0]["status"] == "completed"

def test_categories(mock_task_list):
    with app.test_client() as c:
        response = c.get("/tasks/categories").json
        print(response)
    assert "test" in response[0]
    assert len(response) == 3

def test_by_category(mock_task_list):
    with app.test_client() as c:
        response = c.get("/tasks/categories/test_again").json
    assert len(response) == 1
