# What2Do App - Architecture & Overview

## Project Structure

- **Backend:** Flask API (`app.py`)
- **Frontend:** HTML, CSS, JavaScript (`index.html`, `style.css`, `script.js`)
- **Database:** MySQL
- **Configuration:** Environment variables (`.env`)

## Architecture Overview

### 1. Database

The app uses a MySQL database to store tasks. Each task typically has fields like `id`, `content`, `completed`, and `date_created`. Connection details are managed via environment variables in the `.env` file for security and flexibility.

### 2. Backend (API)

The backend is built with Flask (`app.py`). It exposes RESTful endpoints for managing tasks:

- `GET /tasks` — Fetch all tasks.
- `POST /tasks` — Add a new task.
- `PUT /tasks/<task_id>` — Update a task's completion status.
- `DELETE /tasks/<task_id>` — Delete a task.

The backend connects to MySQL using credentials from `.env`. CORS is enabled to allow requests from the frontend.

### 3. Frontend

The frontend consists of:

- `index.html` — The main HTML structure.
- `style.css` — Styling for the app.
- `script.js` — Handles user interactions and communicates with the backend API using `fetch`.

Users can add, complete, and delete tasks. All actions are sent as HTTP requests to the Flask API, and the UI updates dynamically.

### 4. How It Works

- **User Interaction:** Users interact with the web interface to manage tasks.
- **API Requests:** The frontend sends HTTP requests to the Flask API.
- **Database Operations:** The API performs CRUD operations on the MySQL database.
- **Response:** The API returns JSON responses, which the frontend uses to update the UI.

### 5. Running the App

1. **Install dependencies:**  
   - Python packages: `Flask`, `flask-cors`, `mysql-connector-python`, `python-dotenv`
   - MySQL server

2. **Configure `.env`:**  
   Set your database credentials.

3. **Start the backend:**  
   ```
   python app.py
   ```

4. **Open `index.html` in your browser.**

5. **Using the API:**
To interact directly with the API, use these endpoints:

GET http://localhost:5000/tasks — View all tasks.
POST http://localhost:5000/tasks — Add a task (send JSON).
PUT http://localhost:5000/tasks/<task_id> — Update a task.
DELETE http://localhost:5000/tasks/<task_id> — Delete a task.
You can use tools like Postman, curl, or your browser (for GET requests) to interact with these endpoints.

---

**Note:** Make sure MySQL is running and the required tables exist before starting the app.