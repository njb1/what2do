const API_BASE_URL = 'http://localhost:5000';
//const API_BASE_URL = 'http://http://127.0.0.1:5000';
const taskForm = document.getElementById('task-form');
const newTaskInput = document.getElementById('new-task-input');
const tasksList = document.getElementById('tasks-list');

async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

function displayTasks(tasks) {
    tasksList.innerHTML = '';
    tasks.forEach(task => {
        const taskElement = document.createElement('li');
        taskElement.classList.toggle('completed', task.completed);
        taskElement.setAttribute('data-id', task.id);

        const contentElement = document.createElement('span');
        contentElement.textContent = task.content;
        if (task.completed) {
            contentElement.style.textDecoration = 'line-through';
            contentElement.style.color = '#888';
        }

        const completeButton = document.createElement('button');
        completeButton.textContent = task.completed ? 'Undo' : 'Complete';
        completeButton.addEventListener('click', () => toggleTask(task.id, !task.completed));

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => deleteTask(task.id));

        taskElement.appendChild(contentElement);
        taskElement.appendChild(completeButton);
        taskElement.appendChild(deleteButton);

        tasksList.appendChild(taskElement);
    });
}

async function addTask(content) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content })
        });
        if (response.ok) {
            newTaskInput.value = '';
            fetchTasks();
        }
    } catch (error) {
        console.error('Error adding task:', error);
    }
}

async function toggleTask(taskId, newCompletedStatus) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed: newCompletedStatus })
        });
        if (response.ok) {
            fetchTasks();
        }
    } catch (error) {
        console.error('Error toggling task:', error);
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            fetchTasks();
        }
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

taskForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const content = newTaskInput.value.trim();
    if (content) {
        addTask(content);
    }
});

document.addEventListener('DOMContentLoaded', fetchTasks);
