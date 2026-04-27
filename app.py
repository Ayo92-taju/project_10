from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
from e_service import hash_password, verify_password

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def login_required(role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return "Access denied.", 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'lecturer':
        return redirect(url_for('lecturer_dashboard'))
    elif role == 'student':
        return redirect(url_for('student_dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        conn.close()
        if user and verify_password(password, user['password']):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            return redirect(url_for('home'))
        flash('Invalid email or password.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin/dashboard')
@login_required(role='admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@app.route('/lecturer/dashboard')
@login_required(role='lecturer')
def lecturer_dashboard():
    return render_template('lecturer/dashboard.html')


@app.route('/student/dashboard')
@login_required(role='student')
def student_dashboard():
    return render_template('student/dashboard.html')


@app.route('/admin/departments', methods=['GET'])
@login_required(role='admin')
def get_departments():
    conn = get_db()
    departments = conn.execute('SELECT * FROM departments').fetchall()
    conn.close()
    return render_template('admin/departments.html', departments=departments)


@app.route('/admin/departments', methods=['POST'])
@login_required(role='admin')
def add_department():
    name = request.form['name']
    conn = get_db()
    conn.execute('INSERT INTO departments (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_departments'))


@app.route('/admin/departments/delete/<int:department_id>', methods=['POST'])
@login_required(role='admin')
def delete_department(department_id):
    conn = get_db()
    conn.execute('DELETE FROM departments WHERE id = ?', (department_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_departments'))


@app.route('/admin/sessions', methods=['GET'])
@login_required(role='admin')
def get_sessions():
    conn = get_db()
    sessions = conn.execute('SELECT * FROM sessions').fetchall()
    conn.close()
    return render_template('admin/sessions.html', sessions=sessions)


@app.route('/admin/sessions', methods=['POST'])
@login_required(role='admin')
def add_session():
    academic_year = request.form['academic_year']
    semester = request.form['semester']
    conn = get_db()
    conn.execute('INSERT INTO sessions (academic_year, semester) VALUES (?, ?)', (academic_year, semester))
    conn.commit()
    conn.close()
    return redirect(url_for('get_sessions'))


@app.route('/admin/sessions/delete/<int:session_id>', methods=['POST'])
@login_required(role='admin')
def delete_session(session_id):
    conn = get_db()
    conn.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_sessions'))


@app.route('/admin/sessions/set_current/<int:session_id>', methods=['POST'])
@login_required(role='admin')
def set_current(session_id):
    conn = get_db()
    conn.execute('UPDATE sessions SET is_current = 0')
    conn.execute('UPDATE sessions SET is_current = 1 WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_sessions'))


if __name__ == '__main__':
    app.run(debug=True)