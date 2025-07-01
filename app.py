from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# MongoDB Atlas connection (replace with your connection string)
MONGO_URI = 'mongodb+srv://gnana1313:Gnana1212@dbs.8wngtib.mongodb.net/?retryWrites=true&w=majority&appName=DBs'
client = MongoClient(MONGO_URI)
db = client['timetable']
users_col = db['users']
timetables_col = db['timetables']
tasks_col = db['tasks']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    name = request.form['name']
    gmail = request.form['gmail']
    password = request.form['password']
    if users_col.find_one({'gmail': gmail}):
        flash('Gmail already registered!')
        return redirect(url_for('signup'))
    users_col.insert_one({'name': name, 'gmail': gmail, 'password': password})
    flash('Signup successful! Please login.')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    gmail = request.form['gmail']
    password = request.form['password']
    user = users_col.find_one({'gmail': gmail, 'password': password})
    if user:
        session['user_id'] = str(user['_id'])
        session['name'] = user['name']
        return redirect(url_for('dashboard'))
    flash('Invalid credentials!')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', name=session['name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/create_timetable', methods=['GET', 'POST'])
def create_timetable():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        num_subjects = int(request.form['num_subjects'])
        subject_names = [request.form[f'subject_{i+1}'] for i in range(num_subjects)]
        working_from = request.form['working_from']
        working_to = request.form['working_to']
        days = request.form.getlist('days')
        lunch_duration = int(request.form['lunch_duration'])
        timetable = generate_timetable(subject_names, working_from, working_to, days, lunch_duration)
        timetable_doc = {
            'user_id': session['user_id'],
            'title': title,
            'subjects': subject_names,
            'working_from': working_from,
            'working_to': working_to,
            'days': days,
            'lunch_duration': lunch_duration,
            'timetable': timetable,
            'created_at': datetime.datetime.utcnow()
        }
        timetables_col.insert_one(timetable_doc)
        flash('Timetable created!')
        return render_template('timetable_result.html', timetable=timetable, title=title, days=days)
    return render_template('create_timetable.html')

def generate_timetable(subject_names, working_from, working_to, days, lunch_duration):
    from datetime import datetime, timedelta
    fmt = '%H:%M'
    start = datetime.strptime(working_from, fmt)
    end = datetime.strptime(working_to, fmt)
    total_time = int((end - start).total_seconds() // 60)
    columns_count = len(subject_names) + 1
    duration_per_column = total_time // columns_count
    timetable = []
    for day in days:
        row = []
        current = start
        for i, subject in enumerate(subject_names):
            slot = {'subject': subject, 'from': current.strftime(fmt), 'to': (current + timedelta(minutes=duration_per_column)).strftime(fmt)}
            row.append(slot)
            current += timedelta(minutes=duration_per_column)
            if i == len(subject_names)//2:
                lunch_slot = {'subject': 'Lunch', 'from': current.strftime(fmt), 'to': (current + timedelta(minutes=lunch_duration)).strftime(fmt)}
                row.append(lunch_slot)
                current += timedelta(minutes=lunch_duration)
        timetable.append({'day': day, 'slots': row})
    return timetable

@app.route('/your_timetables')
def your_timetables():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    timetables = list(timetables_col.find({'user_id': session['user_id']}))
    return render_template('your_timetables.html', timetables=timetables)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        subject = request.form['subject']
        tasks_col.insert_one({
            'user_id': session['user_id'],
            'date': date,
            'time': time,
            'subject': subject,
            'status': 'todo'
        })
        return redirect(url_for('tasks'))
    todo_tasks = list(tasks_col.find({'user_id': session['user_id'], 'status': 'todo'}))
    done_tasks = list(tasks_col.find({'user_id': session['user_id'], 'status': 'done'}))
    return render_template('tasks.html', name=session['name'], todo_tasks=todo_tasks, done_tasks=done_tasks)

@app.route('/tasks/done/<task_id>', methods=['POST'])
def mark_task_done(task_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))
    tasks_col.update_one({'_id': ObjectId(task_id), 'user_id': session['user_id']}, {'$set': {'status': 'done'}})
    return redirect(url_for('tasks'))

@app.route('/tasks/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))
    tasks_col.delete_one({'_id': ObjectId(task_id), 'user_id': session['user_id']})
    return redirect(url_for('tasks'))

@app.route('/timetable/delete/<timetable_id>', methods=['POST'])
def delete_timetable(timetable_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))
    timetables_col.delete_one({'_id': ObjectId(timetable_id), 'user_id': session['user_id']})
    return redirect(url_for('your_timetables'))

if __name__ == '__main__':
    app.run(debug=True) 