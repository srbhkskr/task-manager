from unittest.mock import Mock

from test.conftest import client


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Task Manager!"}

def test_create_task(test_db):
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "This is a test task"
    })

    assert response.status_code == 201

def test_create_task_should_fail_on_missing_title(test_db):
    response = client.post("/tasks/", json={
        "description": "This is a test task"
    })
    assert response.status_code == 422


def test_get_tasks(test_db):
    client.post("/tasks/", json={
        "title": "Test Task",
        "description": "This is a test task"
    })

    response = client.get("/tasks/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # At least one task should exist
    assert data[0]["title"] == "Test Task"

    mock_response = Mock()
    response_dict = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    mock_response.json.return_value = response_dict

def test_get_tasks_by_status(test_db):
    client.post("/tasks/", json={
        "title": "Test Task",
        "description": "This is a test task"
    })

    response = client.get("/tasks/?task_status=ToDo")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # At least one task should exist
    assert data[0]["title"] == "Test Task"

    mock_response = Mock()
    response_dict = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    mock_response.json.return_value = response_dict


def test_update_task(test_db):

    client.post("/tasks/", json={
        "title": "Task to Update",
        "description": "This task will be updated",
    })

    task_id = 1
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description",
        "status": "Doing"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"
    assert data["status"] == "Doing"
    assert data["id"] == task_id
    assert "created_at" in data
    assert "updated_at" in data

def test_update_task_status(test_db):

    client.post("/tasks/", json={
        "title": "Task to Update",
        "description": "This task will be updated",
    })

    task_id = 1
    response = client.patch(f"/tasks/{task_id}/status", json={
        "status": "Done"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Task to Update"
    assert data["description"] == "This task will be updated"
    assert data["status"] == "Done"
    assert data["id"] == task_id
    assert "created_at" in data
    assert "updated_at" in data

def test_update_task_should_return_404_on_id_not_found(test_db):

    task_id = 100
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description",
        "status": "Doing"
    })

    assert response.status_code == 404




def test_delete_task(test_db):

    client.post("/tasks/", json={
        "title": "Task to Delete",
        "description": "This task will be updated"
    })

    task_id = 1
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

def test_delete_task_should_return_404_on_id_not_found(test_db):

    task_id = 100
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404

