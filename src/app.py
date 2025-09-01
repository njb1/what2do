from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app and enable CORS
app = Flask(__name__)
# Configuring CORS to allow requests from the frontend application
CORS(app)

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database using credentials and settings
    from environment variables. Defaults are provided for host, user, password, and database
    if environment variables are not set.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection object to the MySQL database.
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'your_mysql_username'),
        password=os.getenv('DB_PASSWORD', 'your_mysql_password'),
        database=os.getenv('DB_NAME', 'todo_app')
    )
    print(f"Connected to database: {connection.database}")
    return connection

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks from the database, ordered by creation date in descending order.
    Returns:
        Response: A JSON response containing a list of tasks.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks ORDER BY date_created DESC')
    tasks = cursor.fetchall()
    print(f"Fetched tasks: {tasks}")
    cursor.close()
    connection.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Handles the creation of a new task via POST request.

    Expects a JSON payload with a 'content' field representing the task description.
    Example JSON Payload:
    {
        "content": "Buy groceries"
    }
    Inserts the new task into the 'tasks' table in the database.
    Returns a JSON response with a success message and HTTP status code 201 upon successful insertion.
    """
    new_task = request.get_json()
    content = new_task['content']
    connection = get_db_connection()
    cursor = connection.cursor()
    print(f"Inserting task with content: {content}")
    print(f"Database before insertion: {connection.database}")
    cursor.execute('INSERT INTO tasks (content) VALUES (%s)', (content,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Task added successfully!'}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update the completion status of a specific task.
    Args:
        task_id (int): The ID of the task to update.
    Request Body (JSON):
        completed (bool): The new completion status for the task.
    Returns:
        Response: A JSON response indicating whether the task was updated successfully.
    """
    updated_data = request.get_json()
    new_completed = updated_data.get('completed')
    connection = get_db_connection()
    cursor = connection.cursor()
    print(f"Updating task ID {task_id} to completed={new_completed}")
    print(f"Database before update: {connection.database}")   
    cursor.execute('UPDATE tasks SET completed = %s WHERE id = %s', (new_completed, task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Task updated successfully!'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Deletes a task from the database by its ID.
    Args:
        task_id (int): The unique identifier of the task to be deleted.
    Returns:
        Response: A JSON response indicating successful deletion of the task.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    print(f"Deleting task ID {task_id}")
    print(f"Database before deletion: {connection.database}")
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Task deleted successfully!'})

@app.route('/')
def index():
    """
    Route handler for the root endpoint ('/').
    Returns a simple message indicating that the What2Do API is running.
    """
    return 'What2Do API is running.'

if __name__ == '__main__':
    """
    Run the Flask application in debug mode if this script is executed directly.
    The application will listen for incoming requests and provide detailed error messages
    in the browser for easier debugging during development.
    """
    app.run(debug=True)