from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLES
def create_tables():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        course TEXT
    )
    """)
    conn.commit()
    conn.close()

create_tables()

# HOME
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        conn.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect('/dashboard')

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template('dashboard.html', students=students)

# ADD STUDENT
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db()
        conn.execute(
            "INSERT INTO students(name,email,course) VALUES (?,?,?)",
            (name, email, course)
        )
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_student.html')

# EDIT STUDENT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn.execute("""
        UPDATE students
        SET name=?, email=?, course=?
        WHERE id=?
        """, (name, email, course, id))

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template('edit_student.html', student=student)

# DELETE
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)