from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "students.db"

# Initialize DB
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        course TEXT NOT NULL
                    )''')
        conn.commit()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
                        (name, email, course))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?",
                        (name, email, course, id))
            conn.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
