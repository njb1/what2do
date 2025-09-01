const API_BASE_URL = 'http://localhost:5000';
// taskForm, newTaskInput, tasksList are references to HTML elements
const taskForm = document.getElementById('task-form'); // Form for adding new tasks
const newTaskInput = document.getElementById('new-task-input'); // Input field for new task content
const tasksList = document.getElementById('tasks-list'); // UL element to display the list of tasks

/**
 * Fetches the list of tasks from the API and displays them.
 * Handles errors by logging them to the console.
 * 
 * @async 
 * @function fetchTasks
 * @returns {Promise<void>} Resolves when tasks are fetched and displayed.
 */
async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

/**
 * Renders a list of tasks in the DOM, updating their display and controls.
 * Each task is shown with its content, a button to toggle completion, and a button to delete.
 * 
 * @param {Array<{id: number|string, content: string, completed: boolean}>} tasks - Array of task objects to display.
 */
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

/**
 * Adds a new task with the specified content to the server.
 * Sends a POST request to the API and refreshes the task list on success.
 *
 * @async
 * @function
 * @param {string} content - The content of the task to add.
 * @returns {Promise<void>} Resolves when the task is added and the list is refreshed.
 */
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

/**
 * Toggles the completion status of a task by sending a PUT request to the API.
 * If the request is successful, refreshes the list of tasks.
 *
 * @async
 * @function toggleTask
 * @param {string|number} taskId - The unique identifier of the task to update.
 * @param {boolean} newCompletedStatus - The new completion status to set for the task.
 * @returns {Promise<void>} Resolves when the operation is complete.
 */
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

/**
 * Deletes a task by its ID from the server.
 *
 * Sends a DELETE request to the API to remove the specified task.
 * If successful, refreshes the task list by calling fetchTasks().
 *
 * @async
 * @function
 * @param {string|number} taskId - The unique identifier of the task to delete.
 * @returns {Promise<void>} Resolves when the task is deleted and the task list is refreshed.
 */
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
    /**
     * The trimmed value from the new task input field.
     * @type {string}
     */
    const content = newTaskInput.value.trim();
    if (content) {
        addTask(content);
    }
});

// Initial fetch of tasks when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', fetchTasks);
