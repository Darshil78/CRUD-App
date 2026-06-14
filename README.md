# CRUD Flask App

A simple Flask-based CRUD application for managing student records with user registration and login.

## Features
- User registration and login
- Session-based authentication
- Add, view, edit, and delete student records
- SQLite database storage

## Project Structure
- app.py - Main Flask application and database setup
- templates/ - HTML templates for login, registration, dashboard, and student forms
- static/ - CSS files for styling
- database.db - SQLite database created automatically on first run

## Requirements
- Python 3.x
- Flask

## Installation
1. Open the project folder.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install Flask:
   ```bash
   pip install flask
   ```

## Run the App
From the project folder, run:
```bash
python app.py
```

Then open your browser and visit:
```text
http://127.0.0.1:5000/
```

## Usage
- Register a new account
- Log in with your credentials
- Use the dashboard to add, edit, or delete student records

## Notes
- The SQLite database file will be created automatically when the app starts.
- The app uses a simple in-memory-style session for authentication.
