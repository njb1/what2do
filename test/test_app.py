# test_app.py

import os
import pytest
import json
from src.app import get_db_connection, app

def test_get_db_connection(monkeypatch):
    # Set environment variables for test
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_USER', 'root')
    monkeypatch.setenv('DB_PASSWORD', 'password')
    monkeypatch.setenv('DB_NAME', 'what2do_app')

    conn = get_db_connection()
    print(f"Connection object: {conn}")
    print(f"Is connected: {conn.is_connected()}")
    print(f"Server info: {conn.server_info}")
    print(f"Database: {conn.database}")
    assert conn is not None
    assert hasattr(conn, 'is_connected')
    assert conn.is_connected()
    conn.close()


def test_get_tasks(client):
    response = client.get('/tasks')
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    assert response.is_json
    tasks = response.get_json()
    assert isinstance(tasks, list)


def test_add_task(client):
    payload = {"content": "Test task"}
    response = client.post('/tasks', json=payload)
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Task added successfully!"
    # Delete the task to clean up
    get_response = client.get('/tasks')
    tasks = get_response.get_json()
    task_id = tasks[0]['id']  # Assuming newest is first due to DESC order
    client.delete(f'/tasks/{task_id}')


def test_update_task(client):
    # First, add a new task to update
    add_response = client.post('/tasks', json={"content": "Task to update"})
    print(f"Add Response status code: {add_response.status_code}")
    assert add_response.status_code == 201
    # Get all tasks and find the last one (just added)
    get_response = client.get('/tasks')
    tasks = get_response.get_json()
    print(f"Tasks: {tasks}")
    print(f"Get Response status code: {get_response.status_code}")
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    task_id = tasks[0]['id']  # Assuming newest is first due to DESC order
    # Update the completion status
    update_response = client.put(f'/tasks/{task_id}', json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.is_json
    data = update_response.get_json()
    assert "message" in data
    assert data["message"] == "Task updated successfully!"
    # Clean up by deleting the task
    client.delete(f'/tasks/{task_id}')


def test_delete_task(client):
    # First, add a new task to ensure there is something to delete
    add_response = client.post('/tasks', json={"content": "Task to delete"})
    print(f"Add Response status code: {add_response.status_code}")
    print(f"Add Response data: {add_response.data}")
    print(f"Add Response JSON: {add_response.get_json()}")
    assert add_response.status_code == 201
    # Get all tasks and find the last one (just added)
    get_response = client.get('/tasks')
    tasks = get_response.get_json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    task_id = tasks[0]['id']  # Assuming newest is first due to DESC order
    # Delete the task
    delete_response = client.delete(f'/tasks/{task_id}')
    print(f"Delete Response status code: {delete_response.status_code}")
    print(f"Delete Response data: {delete_response.data}")
    print(f"Delete Response JSON: {delete_response.get_json()}")
    assert delete_response.status_code == 200
    assert delete_response.is_json
    data = delete_response.get_json()
    assert "message" in data
    assert data["message"] == "Task deleted successfully!"