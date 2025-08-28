# what2do

# Personal Task Manager (To-Do List)

A full-stack web application built with JavaScript, Python, and MySQL. This project demonstrates fundamental CRUD (Create, Read, Update, Delete) operations and API communication between a frontend and backend.

## ✨ Features

-   **View Tasks:** See a list of all your tasks.
-   **Add Task:** Add a new task to the list.
-   **Delete Task:** Remove a task from the list.
-   **Mark Complete/Incomplete:** Toggle the status of a task.

## 🛠️ Tech Stack

-   **Frontend:** JavaScript, HTML, CSS
-   **Backend:** Python
-   **Database:** MySQL
-   **API Communication:** Fetch API, RESTful JSON API

## 📁 Project Structure

```
what2do/
│
├── app.py                 # Flask backend server
├── index.html             # Main frontend HTML file
├── style.css              # CSS styles (optional)
├── script.js              # Frontend JavaScript logic
├── .env                   # Environment variables (for database config)
└── README.md
```

## 🚀 Setup & Installation

### 1. Prerequisites

-   Python 3.x
-   MySQL Server
-   A web browser

### 2. Clone and Setup

```bash
# Create a project directory and navigate into it
mkdir what2do
cd what2do
```

### 3. Database Setup

#### 3.1 Download the Installer:

Go to the official MySQL download page: https://dev.mysql.com/downloads/installer/

You will see two options:

MySQL Installer (web community): A small file that downloads required components as it installs. (Recommended).

MySQL Installer (full): A large offline installer.

Click "Download" for the web community version.

#### 3.2 Run the Installer:

Open the downloaded .msi file.

At the "Choosing a Setup Type" screen, select Developer Default. This will install the MySQL Server, MySQL Shell, and other useful tools like MySQL Workbench (a graphical interface).

Click "Next" and proceed through the steps.

#### 3.3 Product Configuration:

The installer will guide you through configuring the server.

At the "High Availability" screen, choose Standalone MySQL Server / Classic MySQL Replication.

At the "Type and Networking" screen, keep the default settings. Make sure "Use Strong Password Encryption for Authentication" is selected.

#### 3.4 Set the Root Password:

This is the most important step. You will be asked to create a password for the root user.

Choose a strong password and write it down in a secure place! You will need this password to connect to your database from your Python code.

You can also add a MySQL user if you wish, but using root for a local development project is fine.

admin/password
root/password

#### 3.5 Complete the Installation:

Follow the remaining prompts and click "Execute" to install and configure everything.

Once finished, you can check if the MySQL service is running by opening your Start Menu and searching for "Services". Look for "MySQL80" (or a similar name) – its status should be "Running".

1.  Start your MySQL server.
2.  Connect to MySQL and run the following SQL commands to create the database and table:

```sql
CREATE DATABASE what2do_app;
USE what2do_app;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Backend Setup (Flask)

1.  Install the required Python libraries:
    ```bash
    pip install flask mysql-connector-python python-dotenv
    ```
2.  Create a file named `.env` in your project root to store your database credentials:
    ```bash
    DB_HOST=localhost
    DB_USER=your_mysql_username
    DB_PASSWORD=your_mysql_password
    DB_NAME=what2do_app
    ```
    *Replace the values with your actual MySQL credentials.*

3.  Create the Flask server file `app.py` (see code section below).

### 5. Frontend Setup

Create the following files in your project root:
-   `index.html`
-   `script.js`
-   `style.css` (optional, for styling)


## 🏃‍♂️ Running the Application

1.  **Start the Backend Server:**
    ```bash
    python app.py
    ```
    The API will be available at `http://localhost:5000`.

2.  **Serve the Frontend:**
    *Due to CORS, you cannot open `index.html` directly from your file system. Use a simple HTTP server:*
    ```bash
    # In your project directory, run:
    python -m http.server 8000
    ```
3.  **Open the Application:**
    Navigate to `http://localhost:8000` in your web browser.

## 📚 API Endpoints

| Method | Endpoint        | Description                | Body (JSON)                |
| :----- | :-------------- | :------------------------- | :------------------------- |
| GET    | `/tasks`        | Fetch all tasks            | -                          |
| POST   | `/tasks`        | Create a new task          | `{"content": "String"}`    |
| PUT    | `/tasks/<id>`   | Update a task (e.g., toggle complete) | `{"completed": Boolean}` |
| DELETE | `/tasks/<id>`   | Delete a task              | -                          |

## 🔧 Troubleshooting

-   **"CORS" errors in the browser console:** Ensure you have `CORS(app)` in your `app.py` and are viewing the frontend via `http://localhost:8000`, not by double-clicking the HTML file.
-   **MySQL connection errors:** Check your credentials in the `.env` file and ensure your MySQL server is running.
-   **"ModuleNotFoundError: No module named 'flask'":** Ensure you installed the required packages with `pip install`.

## 📖 Resources

-   [Flask Official Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
-   [Using the Fetch API (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
-   [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
