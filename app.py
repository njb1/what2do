from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'your_mysql_username'),
        password=os.getenv('DB_PASSWORD', 'your_mysql_password'),
        database=os.getenv('DB_NAME', 'todo_app')
    )
    return connection

@app.route('/tasks', methods=['GET'])
def get_tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks ORDER BY date_created DESC')
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.get_json()
    content = new_task['content']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tasks (content) VALUES (%s)', (content,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Task added successfully!'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_data = request.get_json()
    new_completed = updated_data.get('completed')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE tasks SET completed = %s WHERE id = %s', (new_completed, task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Task updated successfully!'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Task deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)