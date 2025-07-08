# Smart Timetable Suggestion App

A web application to help users create, manage, and organize their study timetables and tasks efficiently. Built with Flask and MongoDB.

## Features

- **User Authentication**: Sign up, log in, and log out securely.
- **Timetable Creation**: Generate custom timetables based on your subjects, working hours, days, and lunch break.
- **Task Management**: Add, mark as done, and delete study tasks for each subject.
- **Personal Dashboard**: View your timetables and tasks in a user-friendly dashboard.

## Technologies Used

- Python 3
- Flask
- MongoDB (Atlas)
- PyMongo
- HTML/CSS (Jinja2 templates)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Smart-Timetable-Suggestion-App
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB
- The app uses MongoDB Atlas. Update the `MONGO_URI` in `app.py` with your own MongoDB connection string if needed.

### 4. Run the Application
```bash
python app.py
```
- The app will be available at `http://127.0.0.1:5000/`

## Usage

1. **Sign Up**: Register with your name, Gmail, and password.
2. **Log In**: Access your dashboard after logging in.
3. **Create Timetable**: Go to 'Create Timetable', enter your subjects, working hours, days, and lunch duration. Submit to generate a timetable.
4. **View Timetables**: See all your created timetables under 'Your Timetables'.
5. **Manage Tasks**: Add tasks for your study sessions, mark them as done, or delete them as needed.
6. **Logout**: End your session securely.

## File Structure

- `app.py` - Main Flask application.
- `requirements.txt` - Python dependencies.
- `templates/` - HTML templates for the web interface.

