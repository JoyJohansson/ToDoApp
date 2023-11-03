import pytest
from app import app, find_task_by_id, get_all_tasks

task_list = [{"id": 1, "description": "Test first endpoint", "category": "test", "status": "pending"}, 
    {"id": 2, "description": "test second endpoint", "category": "test", "status": "pending"}, 
    {"id": 3, "description": "test third endpoint", "category": "test_again", "status": "complete"}]

@pytest.fixture
def mock_task_list(mocker):
    mocker.patch("app.get_tasks", return_value=task_list)

def test_find_task_by_id(mock_task_list):
    assert find_task_by_id(2) == task_list[1]
    
def test_get_all_tasks(mock_task_list):
    with app.test_request_context("/tasks", method="GET"):
        messages = get_all_tasks()
    assert "Test first endpoint" in messages[0]