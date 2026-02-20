<<<<<<< HEAD
"""
ShikshyaHub — Professional Student Portal System
Flask Backend · SQLite Database · v2.0
Improvements: PDF uploads, eSewa payments, notifications, dark mode
"""

from flask import (Flask, render_template, request, redirect, url_for,
                   session, jsonify, flash, send_from_directory)
from functools import wraps
from werkzeug.utils import secure_filename
import sqlite3, hashlib, os, json, uuid, random, string
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'shikshyahub-secret-key-2024-professional'

DATABASE   = 'shikshyahub.db'
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED    = {'pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg'}

os.makedirs(os.path.join(UPLOAD_DIR, 'assignments'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'materials'),   exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, 'notices'),     exist_ok=True)

# ─── DB helpers ───────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

def save_upload(file, folder):
    """Save an uploaded file and return its stored filename, or None."""
    if not file or file.filename == '':
        return None
    if not allowed_file(file.filename):
        return None
    ext  = file.filename.rsplit('.', 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(UPLOAD_DIR, folder, name))
    return name

# ─── DB init ──────────────────────────────────────────────────────────────────
def init_db():
    conn = get_db()
    c    = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin','teacher','student')),
            phone TEXT, address TEXT, profile_pic TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, description TEXT,
            duration_years INTEGER DEFAULT 4,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, program_id INTEGER,
            semester INTEGER, section TEXT DEFAULT 'A', room TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(program_id) REFERENCES programs(id)
        );
        CREATE TABLE IF NOT EXISTS student_classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, class_id INTEGER,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(class_id) REFERENCES classes(id)
        );
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, code TEXT UNIQUE,
            teacher_id INTEGER, class_id INTEGER,
            description TEXT, syllabus TEXT, credits INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(teacher_id) REFERENCES users(id),
            FOREIGN KEY(class_id) REFERENCES classes(id)
        );
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER, title TEXT NOT NULL,
            file_path TEXT, file_type TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER, title TEXT NOT NULL,
            description TEXT, due_date DATE,
            max_marks INTEGER DEFAULT 100, file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER, student_id INTEGER,
            file_path TEXT, file_name TEXT, notes TEXT,
            marks INTEGER, feedback TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            graded_at TIMESTAMP,
            FOREIGN KEY(assignment_id) REFERENCES assignments(id),
            FOREIGN KEY(student_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, subject_id INTEGER,
            date DATE NOT NULL, status TEXT DEFAULT 'present'
                CHECK(status IN ('present','absent','late')),
            marked_by INTEGER, notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, subject_id INTEGER,
            semester INTEGER,
            internal_marks REAL DEFAULT 0,
            assignment_marks REAL DEFAULT 0,
            exam_marks REAL DEFAULT 0,
            total_marks REAL DEFAULT 0,
            grade TEXT, gpa REAL, published INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, content TEXT NOT NULL,
            audience TEXT DEFAULT 'all'
                CHECK(audience IN ('all','students','teachers','admin')),
            posted_by INTEGER, attachment TEXT, attachment_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(posted_by) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, semester INTEGER,
            total_fee REAL DEFAULT 0, paid_amount REAL DEFAULT 0,
            due_date DATE,
            status TEXT DEFAULT 'pending'
                CHECK(status IN ('pending','paid','partial','overdue')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS fee_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fee_id INTEGER, amount REAL NOT NULL,
            payment_date DATE DEFAULT CURRENT_DATE,
            method TEXT DEFAULT 'cash',
            receipt_no TEXT, transaction_id TEXT, notes TEXT,
            FOREIGN KEY(fee_id) REFERENCES fees(id)
        );
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER, subject_id INTEGER,
            day TEXT NOT NULL, start_time TEXT NOT NULL,
            end_time TEXT NOT NULL, room TEXT,
            FOREIGN KEY(class_id) REFERENCES classes(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, type TEXT NOT NULL,
            title TEXT NOT NULL, message TEXT,
            link TEXT, is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS esewa_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fee_id INTEGER, student_id INTEGER,
            amount REAL NOT NULL,
            transaction_id TEXT UNIQUE,
            ref_id TEXT, status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(fee_id) REFERENCES fees(id),
            FOREIGN KEY(student_id) REFERENCES users(id)
        );
    ''')

    # ── Seed data ──
    if not c.execute("SELECT id FROM users WHERE email='admin@shikshyahub.edu'").fetchone():
        c.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)",
                  ('Super Admin','admin@shikshyahub.edu',hash_password('Admin@123'),'admin'))

        c.execute("INSERT INTO programs (name,description,duration_years) VALUES (?,?,?)",
                  ('Bachelor of Computer Science','BCS Program',4))
        prog_id = c.lastrowid

        c.execute("INSERT INTO classes (name,program_id,semester,section,room) VALUES (?,?,?,?,?)",
                  ('BCS Semester 1',prog_id,1,'A','Room 101'))
        class_id = c.lastrowid

        c.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)",
                  ('Dr. Sarah Johnson','teacher@shikshyahub.edu',hash_password('Teacher@123'),'teacher'))
        teacher_id = c.lastrowid

        c.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)",
                  ('Aayush Sharma','student@shikshyahub.edu',hash_password('Student@123'),'student'))
        student_id = c.lastrowid

        c.execute("INSERT INTO student_classes (student_id,class_id) VALUES (?,?)",(student_id,class_id))

        subjects_seed = [
            ('Introduction to Programming','CS101',teacher_id,class_id,'Learn Python basics',3),
            ('Mathematics I','MATH101',teacher_id,class_id,'Calculus and Algebra',4),
            ('Database Systems','CS201',teacher_id,class_id,'SQL and Database Design',3),
        ]
        for sub in subjects_seed:
            c.execute("INSERT INTO subjects (name,code,teacher_id,class_id,description,credits) VALUES (?,?,?,?,?,?)",sub)
            sub_id = c.lastrowid
            c.execute("INSERT INTO assignments (subject_id,title,description,due_date,max_marks) VALUES (?,?,?,?,?)",
                      (sub_id,f'Assignment 1 — {sub[0]}','Complete the given exercises','2025-12-31',100))
            for i in range(8):
                date   = (datetime.now()-timedelta(days=i)).strftime('%Y-%m-%d')
                status = 'present' if i % 4 != 0 else 'absent'
                c.execute("INSERT INTO attendance (student_id,subject_id,date,status,marked_by) VALUES (?,?,?,?,?)",
                          (student_id,sub_id,date,status,teacher_id))
            c.execute("""INSERT INTO results
                (student_id,subject_id,semester,internal_marks,assignment_marks,
                 exam_marks,total_marks,grade,gpa,published) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                      (student_id,sub_id,1,18,15,55,88,'A',4.0,1))

        c.execute("INSERT INTO fees (student_id,semester,total_fee,paid_amount,due_date,status) VALUES (?,?,?,?,?,?)",
                  (student_id,1,50000,30000,'2025-12-31','partial'))
        fee_id = c.lastrowid
        c.execute("INSERT INTO fee_payments (fee_id,amount,method,receipt_no) VALUES (?,?,?,?)",
                  (fee_id,30000,'esewa','RCP10001'))

        for title,content,audience in [
            ('Welcome to ShikshyaHub','Welcome to our new digital portal!','all'),
            ('Examination Schedule','Final exams start December 15, 2025','students'),
            ('Staff Meeting','All teachers please attend the meeting on Friday','teachers'),
        ]:
            c.execute("INSERT INTO notices (title,content,audience,posted_by) VALUES (?,?,?,?)",
                      (title,content,audience,1))

        days_seed = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        sub_rows  = c.execute("SELECT id FROM subjects WHERE class_id=?",(class_id,)).fetchall()
        for i,day in enumerate(days_seed[:3]):
            for j,sr in enumerate(sub_rows):
                h = 9 + j*2
                c.execute("INSERT INTO timetable (class_id,subject_id,day,start_time,end_time,room) VALUES (?,?,?,?,?,?)",
                          (class_id,sr['id'],day,f'{h:02d}:00',f'{h+1:02d}:30','Room 101'))

        # Seed notifications
        c.execute("INSERT INTO notifications (user_id,type,title,message,link) VALUES (?,?,?,?,?)",
                  (student_id,'notice','New Notice','Welcome to ShikshyaHub!','/student/notices'))
        c.execute("INSERT INTO notifications (user_id,type,title,message,link) VALUES (?,?,?,?,?)",
                  (student_id,'assignment','New Assignment','Check your CS101 assignment','/student/tasks'))

    conn.commit(); conn.close()

# ─── Notification helper ───────────────────────────────────────────────────────
def push_notification(db, user_id, ntype, title, message='', link=''):
    db.execute("INSERT INTO notifications (user_id,type,title,message,link) VALUES (?,?,?,?,?)",
               (user_id,ntype,title,message,link))

def get_unread_count(user_id):
    db = get_db()
    n = db.execute("SELECT COUNT(*) as c FROM notifications WHERE user_id=? AND is_read=0",(user_id,)).fetchone()['c']
    db.close()
    return n

# ─── Auth decorators ──────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def dec(*a,**kw):
        if 'user_id' not in session: return redirect(url_for('login'))
        return f(*a,**kw)
    return dec

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def dec(*a,**kw):
            if 'user_id' not in session: return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('Access denied.','error'); return redirect(url_for('dashboard'))
            return f(*a,**kw)
        return dec
    return decorator

# ─── Context processor: inject notification count into every template ─────────
@app.context_processor
def inject_globals():
    notif_count = 0
    notif_by_type = {}
    if 'user_id' in session:
        db = get_db()
        uid = session['user_id']
        notif_count = db.execute(
            "SELECT COUNT(*) as c FROM notifications WHERE user_id=? AND is_read=0",(uid,)
        ).fetchone()['c']
        rows = db.execute(
            "SELECT type, COUNT(*) as c FROM notifications WHERE user_id=? AND is_read=0 GROUP BY type",(uid,)
        ).fetchall()
        notif_by_type = {r['type']: r['c'] for r in rows}
        db.close()
    return dict(
        notif_count=notif_count,
        notif_by_type=notif_by_type,
        current_year=datetime.now().year
    )

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTES
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email    = request.form.get('email','').strip()
        password = request.form.get('password','')
        db       = get_db()
        user     = db.execute("SELECT * FROM users WHERE email=? AND password_hash=?",
                               (email,hash_password(password))).fetchone()
        db.close()
        if user:
            session.update(user_id=user['id'], name=user['name'],
                           email=user['email'], role=user['role'])
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.','error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    return redirect(url_for('admin_dashboard' if role=='admin'
                             else 'teacher_dashboard' if role=='teacher'
                             else 'student_dashboard'))

# ─── Notifications API ────────────────────────────────────────────────────────
@app.route('/api/notifications')
@login_required
def api_notifications():
    db    = get_db()
    notifs = db.execute("""SELECT * FROM notifications WHERE user_id=?
                            ORDER BY created_at DESC LIMIT 20""",
                         (session['user_id'],)).fetchall()
    unread = db.execute("SELECT COUNT(*) as c FROM notifications WHERE user_id=? AND is_read=0",
                         (session['user_id'],)).fetchone()['c']
    db.close()
    return jsonify({
        'count': unread,
        'items': [dict(n) for n in notifs]
    })

@app.route('/api/notifications/read', methods=['POST'])
@login_required
def api_mark_notifications_read():
    db = get_db()
    db.execute("UPDATE notifications SET is_read=1 WHERE user_id=?",(session['user_id'],))
    db.commit(); db.close()
    return jsonify({'ok': True})

# ─── File download route ──────────────────────────────────────────────────────
@app.route('/uploads/<folder>/<filename>')
@login_required
def serve_upload(folder, filename):
    path = os.path.join(UPLOAD_DIR, folder)
    return send_from_directory(path, filename)

# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN ROUTES
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/admin')
@role_required('admin')
def admin_dashboard():
    db   = get_db()
    stats = {
        'students': db.execute("SELECT COUNT(*) as c FROM users WHERE role='student'").fetchone()['c'],
        'teachers': db.execute("SELECT COUNT(*) as c FROM users WHERE role='teacher'").fetchone()['c'],
        'subjects': db.execute("SELECT COUNT(*) as c FROM subjects").fetchone()['c'],
        'classes':  db.execute("SELECT COUNT(*) as c FROM classes").fetchone()['c'],
    }
    recent_notices  = db.execute("SELECT * FROM notices ORDER BY created_at DESC LIMIT 5").fetchall()
    recent_students = db.execute("SELECT * FROM users WHERE role='student' ORDER BY created_at DESC LIMIT 5").fetchall()
    fees_overview   = db.execute("SELECT SUM(total_fee) as total, SUM(paid_amount) as paid FROM fees").fetchone()
    att_total       = db.execute("SELECT COUNT(*) as c FROM attendance").fetchone()['c']
    att_present     = db.execute("SELECT COUNT(*) as c FROM attendance WHERE status='present'").fetchone()['c']
    att_pct         = round((att_present/att_total*100) if att_total else 0, 1)
    db.close()
    return render_template('admin/dashboard.html', stats=stats,
                           recent_notices=recent_notices, recent_students=recent_students,
                           fees_overview=fees_overview, att_pct=att_pct)

@app.route('/admin/students')
@role_required('admin')
def admin_students():
    db = get_db()
    students = db.execute("""
        SELECT u.*, c.name as class_name FROM users u
        LEFT JOIN student_classes sc ON sc.student_id=u.id
        LEFT JOIN classes c ON c.id=sc.class_id
        WHERE u.role='student' ORDER BY u.created_at DESC""").fetchall()
    classes = db.execute("SELECT * FROM classes").fetchall()
    db.close()
    return render_template('admin/students.html', students=students, classes=classes)

@app.route('/admin/students/create', methods=['POST'])
@role_required('admin')
def admin_create_student():
    db = get_db()
    try:
        db.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)",
                   (request.form['name'], request.form['email'],
                    hash_password(request.form['password']), 'student'))
        sid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        if request.form.get('class_id'):
            db.execute("INSERT INTO student_classes (student_id,class_id) VALUES (?,?)",
                       (sid, request.form['class_id']))
        db.commit(); flash('Student created!','success')
    except Exception as e:
        flash(f'Error: {e}','error')
    db.close()
    return redirect(url_for('admin_students'))

@app.route('/admin/students/delete/<int:sid>', methods=['POST'])
@role_required('admin')
def admin_delete_student(sid):
    db = get_db()
    db.execute("DELETE FROM student_classes WHERE student_id=?",(sid,))
    db.execute("DELETE FROM users WHERE id=? AND role='student'",(sid,))
    db.commit(); db.close()
    flash('Student deleted.','success')
    return redirect(url_for('admin_students'))

@app.route('/admin/teachers')
@role_required('admin')
def admin_teachers():
    db = get_db()
    teachers = db.execute("""
        SELECT u.*, COUNT(s.id) as subject_count FROM users u
        LEFT JOIN subjects s ON s.teacher_id=u.id
        WHERE u.role='teacher' GROUP BY u.id ORDER BY u.created_at DESC""").fetchall()
    db.close()
    return render_template('admin/teachers.html', teachers=teachers)

@app.route('/admin/teachers/create', methods=['POST'])
@role_required('admin')
def admin_create_teacher():
    db = get_db()
    try:
        db.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)",
                   (request.form['name'],request.form['email'],
                    hash_password(request.form['password']),'teacher'))
        db.commit(); flash('Teacher created!','success')
    except Exception as e:
        flash(f'Error: {e}','error')
    db.close()
    return redirect(url_for('admin_teachers'))

@app.route('/admin/teachers/delete/<int:tid>', methods=['POST'])
@role_required('admin')
def admin_delete_teacher(tid):
    db = get_db()
    db.execute("DELETE FROM users WHERE id=? AND role='teacher'",(tid,))
    db.commit(); db.close()
    flash('Teacher deleted.','success')
    return redirect(url_for('admin_teachers'))

@app.route('/admin/subjects')
@role_required('admin')
def admin_subjects():
    db = get_db()
    subjects  = db.execute("""
        SELECT s.*,u.name as teacher_name,c.name as class_name FROM subjects s
        LEFT JOIN users u ON u.id=s.teacher_id
        LEFT JOIN classes c ON c.id=s.class_id ORDER BY s.created_at DESC""").fetchall()
    teachers = db.execute("SELECT id,name FROM users WHERE role='teacher'").fetchall()
    classes  = db.execute("SELECT * FROM classes").fetchall()
    db.close()
    return render_template('admin/subjects.html', subjects=subjects,
                           teachers=teachers, classes=classes)

@app.route('/admin/subjects/create', methods=['POST'])
@role_required('admin')
def admin_create_subject():
    db = get_db()
    try:
        db.execute("INSERT INTO subjects (name,code,teacher_id,class_id,description,credits) VALUES (?,?,?,?,?,?)",
                   (request.form['name'], request.form['code'],
                    request.form.get('teacher_id') or None,
                    request.form.get('class_id') or None,
                    request.form.get('description'), request.form.get('credits',3)))
        db.commit(); flash('Subject created!','success')
    except Exception as e:
        flash(f'Error: {e}','error')
    db.close()
    return redirect(url_for('admin_subjects'))

@app.route('/admin/subjects/delete/<int:sid>', methods=['POST'])
@role_required('admin')
def admin_delete_subject(sid):
    db = get_db()
    db.execute("DELETE FROM subjects WHERE id=?",(sid,))
    db.commit(); db.close()
    flash('Subject deleted.','success')
    return redirect(url_for('admin_subjects'))

@app.route('/admin/classes')
@role_required('admin')
def admin_classes():
    db = get_db()
    classes  = db.execute("""
        SELECT c.*,p.name as program_name,COUNT(sc.student_id) as student_count FROM classes c
        LEFT JOIN programs p ON p.id=c.program_id
        LEFT JOIN student_classes sc ON sc.class_id=c.id
        GROUP BY c.id ORDER BY c.created_at DESC""").fetchall()
    programs = db.execute("SELECT * FROM programs").fetchall()
    db.close()
    return render_template('admin/classes.html', classes=classes, programs=programs)

@app.route('/admin/classes/create', methods=['POST'])
@role_required('admin')
def admin_create_class():
    db = get_db()
    db.execute("INSERT INTO classes (name,program_id,semester,section,room) VALUES (?,?,?,?,?)",
               (request.form['name'], request.form.get('program_id') or None,
                request.form.get('semester',1), request.form.get('section','A'),
                request.form.get('room')))
    db.commit(); db.close()
    flash('Class created!','success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/programs/create', methods=['POST'])
@role_required('admin')
def admin_create_program():
    db = get_db()
    db.execute("INSERT INTO programs (name,description,duration_years) VALUES (?,?,?)",
               (request.form['name'], request.form.get('description'),
                request.form.get('duration_years',4)))
    db.commit(); db.close()
    flash('Program created!','success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/attendance')
@role_required('admin')
def admin_attendance():
    db = get_db()
    attendance = db.execute("""
        SELECT a.*,u.name as student_name,s.name as subject_name FROM attendance a
        JOIN users u ON u.id=a.student_id JOIN subjects s ON s.id=a.subject_id
        ORDER BY a.date DESC LIMIT 100""").fetchall()
    total   = db.execute("SELECT COUNT(*) as c FROM attendance").fetchone()['c']
    present = db.execute("SELECT COUNT(*) as c FROM attendance WHERE status='present'").fetchone()['c']
    absent  = db.execute("SELECT COUNT(*) as c FROM attendance WHERE status='absent'").fetchone()['c']
    students = db.execute("SELECT id,name FROM users WHERE role='student'").fetchall()
    subjects = db.execute("SELECT id,name FROM subjects").fetchall()
    db.close()
    return render_template('admin/attendance.html', attendance=attendance,
                           students=students, subjects=subjects,
                           total=total, present=present, absent=absent)

@app.route('/admin/notices')
@role_required('admin')
def admin_notices():
    db = get_db()
    notices = db.execute("""
        SELECT n.*,u.name as posted_by_name FROM notices n
        LEFT JOIN users u ON u.id=n.posted_by ORDER BY n.created_at DESC""").fetchall()
    db.close()
    return render_template('admin/notices.html', notices=notices)

@app.route('/admin/notices/create', methods=['POST'])
@role_required('admin')
def admin_create_notice():
    db = get_db()
    attachment = None; attachment_name = None
    if 'attachment' in request.files:
        f = request.files['attachment']
        saved = save_upload(f, 'notices')
        if saved:
            attachment      = saved
            attachment_name = secure_filename(f.filename)
    audience = request.form.get('audience','all')
    db.execute("INSERT INTO notices (title,content,audience,posted_by,attachment,attachment_name) VALUES (?,?,?,?,?,?)",
               (request.form['title'], request.form['content'],
                audience, session['user_id'], attachment, attachment_name))
    nid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    # Push notification to relevant users
    if audience in ('all','students'):
        students = db.execute("SELECT id FROM users WHERE role='student'").fetchall()
        for s in students:
            push_notification(db, s['id'], 'notice', request.form['title'],
                              request.form['content'][:80], '/student/notices')
    if audience in ('all','teachers'):
        teachers = db.execute("SELECT id FROM users WHERE role='teacher'").fetchall()
        for t in teachers:
            push_notification(db, t['id'], 'notice', request.form['title'],
                              request.form['content'][:80], '/teacher/notices')
    db.commit(); db.close()
    flash('Notice posted!','success')
    return redirect(url_for('admin_notices'))

@app.route('/admin/notices/delete/<int:nid>', methods=['POST'])
@role_required('admin')
def admin_delete_notice(nid):
    db = get_db()
    db.execute("DELETE FROM notices WHERE id=?",(nid,))
    db.commit(); db.close()
    flash('Notice deleted.','success')
    return redirect(url_for('admin_notices'))

@app.route('/admin/fees')
@role_required('admin')
def admin_fees():
    db = get_db()
    fees     = db.execute("""
        SELECT f.*,u.name as student_name FROM fees f
        JOIN users u ON u.id=f.student_id ORDER BY f.created_at DESC""").fetchall()
    students = db.execute("SELECT id,name FROM users WHERE role='student'").fetchall()
    overview = db.execute("SELECT SUM(total_fee) as total,SUM(paid_amount) as paid FROM fees").fetchone()
    db.close()
    return render_template('admin/fees.html', fees=fees, students=students, overview=overview)

@app.route('/admin/fees/create', methods=['POST'])
@role_required('admin')
def admin_create_fee():
    db = get_db()
    db.execute("INSERT INTO fees (student_id,semester,total_fee,paid_amount,due_date,status) VALUES (?,?,?,?,?,?)",
               (request.form['student_id'], request.form.get('semester',1),
                request.form['total_fee'], request.form.get('paid_amount',0),
                request.form.get('due_date'), 'pending'))
    db.commit(); db.close()
    flash('Fee record created!','success')
    return redirect(url_for('admin_fees'))

@app.route('/admin/fees/pay/<int:fid>', methods=['POST'])
@role_required('admin')
def admin_record_payment(fid):
    db     = get_db()
    amount = float(request.form['amount'])
    fee    = db.execute("SELECT * FROM fees WHERE id=?",(fid,)).fetchone()
    new_paid = fee['paid_amount'] + amount
    status   = 'paid' if new_paid >= fee['total_fee'] else 'partial'
    db.execute("UPDATE fees SET paid_amount=?,status=? WHERE id=?",(new_paid,status,fid))
    receipt = 'RCP' + ''.join(random.choices(string.digits, k=6))
    db.execute("INSERT INTO fee_payments (fee_id,amount,method,receipt_no) VALUES (?,?,?,?)",
               (fid, amount, 'cash', receipt))
    push_notification(db, fee['student_id'], 'fee',
                      'Payment Recorded', f'Rs {amount:,.0f} payment recorded. Receipt: {receipt}',
                      '/student/fees')
    db.commit(); db.close()
    flash(f'Payment recorded! Receipt: {receipt}','success')
    return redirect(url_for('admin_fees'))

@app.route('/admin/results')
@role_required('admin')
def admin_results():
    db = get_db()
    results = db.execute("""
        SELECT r.*,u.name as student_name,s.name as subject_name FROM results r
        JOIN users u ON u.id=r.student_id JOIN subjects s ON s.id=r.subject_id
        ORDER BY r.created_at DESC""").fetchall()
    db.close()
    return render_template('admin/results.html', results=results)

@app.route('/admin/results/publish/<int:rid>', methods=['POST'])
@role_required('admin')
def admin_publish_result(rid):
    db  = get_db()
    res = db.execute("SELECT r.*,s.name as sname FROM results r JOIN subjects s ON s.id=r.subject_id WHERE r.id=?",(rid,)).fetchone()
    db.execute("UPDATE results SET published=1 WHERE id=?",(rid,))
    push_notification(db, res['student_id'], 'result',
                      'Result Published', f'Your result for {res["sname"]} is now available.',
                      '/student/results')
    db.commit(); db.close()
    flash('Result published!','success')
    return redirect(url_for('admin_results'))

@app.route('/admin/timetable')
@role_required('admin')
def admin_timetable():
    db = get_db()
    timetable = db.execute("""
        SELECT t.*,c.name as class_name,s.name as subject_name,u.name as teacher_name FROM timetable t
        JOIN classes c ON c.id=t.class_id JOIN subjects s ON s.id=t.subject_id
        LEFT JOIN users u ON u.id=s.teacher_id ORDER BY t.day,t.start_time""").fetchall()
    classes  = db.execute("SELECT * FROM classes").fetchall()
    subjects = db.execute("SELECT s.*,u.name as teacher_name FROM subjects s LEFT JOIN users u ON u.id=s.teacher_id").fetchall()
    db.close()
    return render_template('admin/timetable.html', timetable=timetable,
                           classes=classes, subjects=subjects)

@app.route('/admin/timetable/create', methods=['POST'])
@role_required('admin')
def admin_create_timetable():
    db = get_db()
    db.execute("INSERT INTO timetable (class_id,subject_id,day,start_time,end_time,room) VALUES (?,?,?,?,?,?)",
               (request.form['class_id'], request.form['subject_id'],
                request.form['day'], request.form['start_time'],
                request.form['end_time'], request.form.get('room')))
    db.commit(); db.close()
    flash('Timetable entry added!','success')
    return redirect(url_for('admin_timetable'))

@app.route('/admin/assignments')
@role_required('admin')
def admin_assignments():
    db = get_db()
    assignments = db.execute("""
        SELECT a.*,s.name as subject_name,u.name as teacher_name,
               COUNT(sub.id) as submission_count FROM assignments a
        JOIN subjects s ON s.id=a.subject_id LEFT JOIN users u ON u.id=s.teacher_id
        LEFT JOIN submissions sub ON sub.assignment_id=a.id
        GROUP BY a.id ORDER BY a.created_at DESC""").fetchall()
    db.close()
    return render_template('admin/assignments.html', assignments=assignments)

# ═══════════════════════════════════════════════════════════════════════════════
# TEACHER ROUTES
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/teacher')
@role_required('teacher')
def teacher_dashboard():
    db      = get_db()
    tid     = session['user_id']
    subjects = db.execute("SELECT * FROM subjects WHERE teacher_id=?",(tid,)).fetchall()
    today   = datetime.now().strftime('%A')
    today_classes = db.execute("""
        SELECT t.*,s.name as subject_name,c.name as class_name FROM timetable t
        JOIN subjects s ON s.id=t.subject_id JOIN classes c ON c.id=t.class_id
        WHERE s.teacher_id=? AND t.day=?""",(tid,today)).fetchall()
    pending_grading = db.execute("""
        SELECT COUNT(*) as c FROM submissions sub
        JOIN assignments a ON a.id=sub.assignment_id
        JOIN subjects s ON s.id=a.subject_id
        WHERE s.teacher_id=? AND sub.marks IS NULL""",(tid,)).fetchone()['c']
    notices = db.execute("""
        SELECT n.*,u.name as posted_by_name FROM notices n LEFT JOIN users u ON u.id=n.posted_by
        WHERE n.audience IN ('all','teachers') ORDER BY n.created_at DESC LIMIT 5""").fetchall()
    db.close()
    return render_template('teacher/dashboard.html', subjects=subjects,
                           today_classes=today_classes, pending_grading=pending_grading,
                           notices=notices)

@app.route('/teacher/subjects')
@role_required('teacher')
def teacher_subjects():
    db  = get_db()
    tid = session['user_id']
    subjects = db.execute("""
        SELECT s.*,c.name as class_name,COUNT(DISTINCT sc.student_id) as student_count
        FROM subjects s LEFT JOIN classes c ON c.id=s.class_id
        LEFT JOIN student_classes sc ON sc.class_id=s.class_id
        WHERE s.teacher_id=? GROUP BY s.id""",(tid,)).fetchall()
    db.close()
    return render_template('teacher/subjects.html', subjects=subjects)

@app.route('/teacher/subjects/<int:sid>')
@role_required('teacher')
def teacher_subject_detail(sid):
    db = get_db()
    subject = db.execute("SELECT s.*,c.name as class_name FROM subjects s LEFT JOIN classes c ON c.id=s.class_id WHERE s.id=?",(sid,)).fetchone()
    if not subject or subject['teacher_id'] != session['user_id']:
        flash('Access denied.','error'); return redirect(url_for('teacher_subjects'))
    materials   = db.execute("SELECT * FROM materials WHERE subject_id=? ORDER BY uploaded_at DESC",(sid,)).fetchall()
    assignments = db.execute("""
        SELECT a.*,COUNT(sub.id) as sub_count FROM assignments a
        LEFT JOIN submissions sub ON sub.assignment_id=a.id
        WHERE a.subject_id=? GROUP BY a.id ORDER BY a.created_at DESC""",(sid,)).fetchall()
    students = db.execute("""
        SELECT u.* FROM users u JOIN student_classes sc ON sc.student_id=u.id
        WHERE sc.class_id=?""",(subject['class_id'],)).fetchall()
    db.close()
    return render_template('teacher/subject_detail.html', subject=subject,
                           materials=materials, assignments=assignments, students=students)

@app.route('/teacher/materials/upload', methods=['POST'])
@role_required('teacher')
def teacher_upload_material():
    db = get_db()
    subject_id = request.form['subject_id']
    title      = request.form['title']
    saved = None; ftype = None
    if 'file' in request.files:
        f     = request.files['file']
        saved = save_upload(f, 'materials')
        if saved:
            ftype = f.filename.rsplit('.', 1)[1].lower()
    if saved:
        db.execute("INSERT INTO materials (subject_id,title,file_path,file_type) VALUES (?,?,?,?)",
                   (subject_id, title, saved, ftype))
        db.commit()
        flash('Material uploaded!','success')
    else:
        flash('Please upload a valid file (PDF, DOC, DOCX, PPT, PPTX, etc.)','error')
    db.close()
    return redirect(url_for('teacher_subject_detail', sid=subject_id))

@app.route('/teacher/assignments/create', methods=['POST'])
@role_required('teacher')
def teacher_create_assignment():
    db = get_db()
    subject_id = request.form['subject_id']
    saved = None
    if 'file' in request.files:
        saved = save_upload(request.files['file'], 'assignments')
    db.execute("INSERT INTO assignments (subject_id,title,description,due_date,max_marks,file_path) VALUES (?,?,?,?,?,?)",
               (subject_id, request.form['title'], request.form.get('description'),
                request.form.get('due_date'), request.form.get('max_marks',100), saved))
    aid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    # Notify enrolled students
    students = db.execute("""
        SELECT u.id FROM users u JOIN student_classes sc ON sc.student_id=u.id
        JOIN subjects s ON s.class_id=sc.class_id WHERE s.id=?""",(subject_id,)).fetchall()
    for s in students:
        push_notification(db, s['id'], 'assignment',
                          f'New Assignment', request.form['title'], '/student/tasks')
    db.commit(); db.close()
    flash('Assignment created!','success')
    return redirect(url_for('teacher_subject_detail', sid=subject_id))

@app.route('/teacher/assignments/<int:aid>/submissions')
@role_required('teacher')
def teacher_view_submissions(aid):
    db = get_db()
    assignment = db.execute("""
        SELECT a.*,s.name as subject_name,s.id as subject_id FROM assignments a
        JOIN subjects s ON s.id=a.subject_id WHERE a.id=?""",(aid,)).fetchone()
    submissions = db.execute("""
        SELECT sub.*,u.name as student_name FROM submissions sub
        JOIN users u ON u.id=sub.student_id
        WHERE sub.assignment_id=? ORDER BY sub.submitted_at DESC""",(aid,)).fetchall()
    db.close()
    return render_template('teacher/submissions.html', assignment=assignment, submissions=submissions)

@app.route('/teacher/submissions/grade/<int:subid>', methods=['POST'])
@role_required('teacher')
def teacher_grade_submission(subid):
    db  = get_db()
    sub = db.execute("SELECT sub.*,a.subject_id FROM submissions sub JOIN assignments a ON a.id=sub.assignment_id WHERE sub.id=?",(subid,)).fetchone()
    db.execute("UPDATE submissions SET marks=?,feedback=?,graded_at=CURRENT_TIMESTAMP WHERE id=?",
               (request.form['marks'], request.form.get('feedback'), subid))
    push_notification(db, sub['student_id'], 'grade',
                      'Assignment Graded', f'You received {request.form["marks"]} marks.',
                      '/student/tasks')
    aid = sub['assignment_id']
    db.commit(); db.close()
    flash('Graded!','success')
    return redirect(url_for('teacher_view_submissions', aid=aid))

@app.route('/teacher/attendance')
@role_required('teacher')
def teacher_attendance():
    db  = get_db()
    tid = session['user_id']
    subjects  = db.execute("SELECT * FROM subjects WHERE teacher_id=?",(tid,)).fetchall()
    attendance = db.execute("""
        SELECT a.*,u.name as student_name,s.name as subject_name FROM attendance a
        JOIN users u ON u.id=a.student_id JOIN subjects s ON s.id=a.subject_id
        WHERE s.teacher_id=? ORDER BY a.date DESC LIMIT 50""",(tid,)).fetchall()
    students = db.execute("""
        SELECT DISTINCT u.id,u.name FROM users u
        JOIN student_classes sc ON sc.student_id=u.id
        JOIN subjects s ON s.class_id=sc.class_id WHERE s.teacher_id=?""",(tid,)).fetchall()
    db.close()
    return render_template('teacher/attendance.html', subjects=subjects,
                           attendance=attendance, students=students)

@app.route('/teacher/attendance/mark', methods=['POST'])
@role_required('teacher')
def teacher_mark_attendance():
    db         = get_db()
    subject_id = request.form['subject_id']
    date       = request.form['date']
    student_ids = request.form.getlist('student_ids[]')
    statuses    = request.form.getlist('statuses[]')
    for sid, status in zip(student_ids, statuses):
        ex = db.execute("SELECT id FROM attendance WHERE student_id=? AND subject_id=? AND date=?",(sid,subject_id,date)).fetchone()
        if ex:
            db.execute("UPDATE attendance SET status=?,marked_by=? WHERE id=?",(status,session['user_id'],ex['id']))
        else:
            db.execute("INSERT INTO attendance (student_id,subject_id,date,status,marked_by) VALUES (?,?,?,?,?)",
                       (sid,subject_id,date,status,session['user_id']))
    db.commit(); db.close()
    flash('Attendance marked!','success')
    return redirect(url_for('teacher_attendance'))

@app.route('/teacher/results')
@role_required('teacher')
def teacher_results():
    db  = get_db()
    tid = session['user_id']
    results  = db.execute("""
        SELECT r.*,u.name as student_name,s.name as subject_name FROM results r
        JOIN users u ON u.id=r.student_id JOIN subjects s ON s.id=r.subject_id
        WHERE s.teacher_id=? ORDER BY r.created_at DESC""",(tid,)).fetchall()
    subjects = db.execute("SELECT * FROM subjects WHERE teacher_id=?",(tid,)).fetchall()
    students = db.execute("""
        SELECT DISTINCT u.id,u.name FROM users u
        JOIN student_classes sc ON sc.student_id=u.id
        JOIN subjects s ON s.class_id=sc.class_id WHERE s.teacher_id=?""",(tid,)).fetchall()
    db.close()
    return render_template('teacher/results.html', results=results,
                           subjects=subjects, students=students)

@app.route('/teacher/results/add', methods=['POST'])
@role_required('teacher')
def teacher_add_result():
    db = get_db()
    i = float(request.form.get('internal_marks',0))
    a = float(request.form.get('assignment_marks',0))
    e = float(request.form.get('exam_marks',0))
    total = i + a + e
    grade = ('A+' if total>=90 else 'A' if total>=80 else 'B+' if total>=70
             else 'B' if total>=60 else 'C' if total>=50 else 'F')
    gpa   = (4.0 if total>=90 else 3.7 if total>=85 else 3.3 if total>=80
             else 3.0 if total>=75 else 2.7 if total>=70 else 2.3 if total>=65
             else 2.0 if total>=60 else 1.0 if total>=50 else 0.0)
    try:
        db.execute("""INSERT INTO results
            (student_id,subject_id,semester,internal_marks,assignment_marks,
             exam_marks,total_marks,grade,gpa) VALUES (?,?,?,?,?,?,?,?,?)""",
            (request.form['student_id'], request.form['subject_id'],
             request.form.get('semester',1), i, a, e, total, grade, gpa))
        db.commit(); flash('Result added!','success')
    except Exception as ex:
        flash(f'Error: {ex}','error')
    db.close()
    return redirect(url_for('teacher_results'))

@app.route('/teacher/notices')
@role_required('teacher')
def teacher_notices():
    db = get_db()
    notices = db.execute("""
        SELECT n.*,u.name as posted_by_name FROM notices n LEFT JOIN users u ON u.id=n.posted_by
        WHERE n.audience IN ('all','students','teachers') ORDER BY n.created_at DESC""").fetchall()
    db.close()
    return render_template('teacher/notices.html', notices=notices)

@app.route('/teacher/notices/create', methods=['POST'])
@role_required('teacher')
def teacher_create_notice():
    db = get_db()
    attachment = save_upload(request.files.get('attachment'), 'notices') if 'attachment' in request.files else None
    attachment_name = secure_filename(request.files['attachment'].filename) if attachment else None
    audience = request.form.get('audience','students')
    db.execute("INSERT INTO notices (title,content,audience,posted_by,attachment,attachment_name) VALUES (?,?,?,?,?,?)",
               (request.form['title'], request.form['content'],
                audience, session['user_id'], attachment, attachment_name))
    db.commit()
    if audience in ('all','students'):
        students = db.execute("SELECT id FROM users WHERE role='student'").fetchall()
        for s in students:
            push_notification(db, s['id'], 'notice', request.form['title'],
                              request.form['content'][:80], '/student/notices')
    db.commit(); db.close()
    flash('Notice posted!','success')
    return redirect(url_for('teacher_notices'))

# ═══════════════════════════════════════════════════════════════════════════════
# STUDENT ROUTES
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/student')
@role_required('student')
def student_dashboard():
    db   = get_db()
    sid  = session['user_id']
    class_info = db.execute("""
        SELECT c.* FROM classes c JOIN student_classes sc ON sc.class_id=c.id
        WHERE sc.student_id=?""",(sid,)).fetchone()
    subjects = []
    if class_info:
        subjects = db.execute("SELECT * FROM subjects WHERE class_id=?",(class_info['id'],)).fetchall()
    total_att   = db.execute("SELECT COUNT(*) as c FROM attendance WHERE student_id=?",(sid,)).fetchone()['c']
    present_att = db.execute("SELECT COUNT(*) as c FROM attendance WHERE student_id=? AND status='present'",(sid,)).fetchone()['c']
    att_pct     = round((present_att/total_att*100) if total_att else 0, 1)
    pending = 0
    if class_info:
        pending = db.execute("""
            SELECT COUNT(*) as c FROM assignments a JOIN subjects s ON s.id=a.subject_id
            WHERE s.class_id=? AND a.id NOT IN
                (SELECT assignment_id FROM submissions WHERE student_id=?)
            AND (a.due_date IS NULL OR a.due_date >= date('now'))""",
            (class_info['id'], sid)).fetchone()['c']
    notices = db.execute("""
        SELECT n.*,u.name as posted_by_name FROM notices n LEFT JOIN users u ON u.id=n.posted_by
        WHERE n.audience IN ('all','students') ORDER BY n.created_at DESC LIMIT 5""").fetchall()
    fee_info = db.execute("SELECT * FROM fees WHERE student_id=? ORDER BY created_at DESC LIMIT 1",(sid,)).fetchone()
    today    = datetime.now().strftime('%A')
    today_schedule = []
    if class_info:
        today_schedule = db.execute("""
            SELECT t.*,s.name as subject_name,u.name as teacher_name FROM timetable t
            JOIN subjects s ON s.id=t.subject_id LEFT JOIN users u ON u.id=s.teacher_id
            WHERE t.class_id=? AND t.day=? ORDER BY t.start_time""",
            (class_info['id'],today)).fetchall()
    db.close()
    return render_template('student/dashboard.html', subjects=subjects, att_pct=att_pct,
                           pending=pending, notices=notices, fee_info=fee_info,
                           today_schedule=today_schedule, class_info=class_info)

@app.route('/student/subjects')
@role_required('student')
def student_subjects():
    db  = get_db()
    sid = session['user_id']
    class_info = db.execute("""
        SELECT c.* FROM classes c JOIN student_classes sc ON sc.class_id=c.id
        WHERE sc.student_id=?""",(sid,)).fetchone()
    subjects = []
    if class_info:
        subjects = db.execute("""
            SELECT s.*,u.name as teacher_name FROM subjects s
            LEFT JOIN users u ON u.id=s.teacher_id WHERE s.class_id=?""",
            (class_info['id'],)).fetchall()
    db.close()
    return render_template('student/subjects.html', subjects=subjects, class_info=class_info)

@app.route('/student/subjects/<int:sid>')
@role_required('student')
def student_subject_detail(sid):
    db         = get_db()
    student_id = session['user_id']
    subject    = db.execute("SELECT s.*,u.name as teacher_name FROM subjects s LEFT JOIN users u ON u.id=s.teacher_id WHERE s.id=?",(sid,)).fetchone()
    materials  = db.execute("SELECT * FROM materials WHERE subject_id=? ORDER BY uploaded_at DESC",(sid,)).fetchall()
    assignments = db.execute("""
        SELECT a.*,sub.id as submission_id,sub.marks,sub.feedback,sub.submitted_at,
               sub.file_name as sub_file FROM assignments a
        LEFT JOIN submissions sub ON sub.assignment_id=a.id AND sub.student_id=?
        WHERE a.subject_id=? ORDER BY a.due_date""",(student_id,sid)).fetchall()
    db.close()
    return render_template('student/subject_detail.html', subject=subject,
                           materials=materials, assignments=assignments)

@app.route('/student/assignments/submit', methods=['POST'])
@role_required('student')
def student_submit_assignment():
    db  = get_db()
    sid = session['user_id']
    aid = request.form['assignment_id']
    notes = request.form.get('notes','')
    existing = db.execute("SELECT id FROM submissions WHERE student_id=? AND assignment_id=?",(sid,aid)).fetchone()
    if existing:
        flash('Already submitted.','info')
    else:
        saved = None; fname = None
        if 'file' in request.files:
            f = request.files['file']
            if f and f.filename:
                saved = save_upload(f, 'assignments')
                fname = secure_filename(f.filename) if saved else None
        if not saved and not notes:
            flash('Please upload a file or add notes.','error')
        else:
            db.execute("INSERT INTO submissions (assignment_id,student_id,file_path,file_name,notes) VALUES (?,?,?,?,?)",
                       (aid, sid, saved, fname, notes))
            db.commit()
            flash('Assignment submitted successfully!','success')
    db.close()
    sub_info = get_db().execute("SELECT subject_id FROM assignments WHERE id=?",(aid,)).fetchone()
    get_db().close()
    return redirect(url_for('student_subject_detail', sid=sub_info['subject_id']))

@app.route('/student/attendance')
@role_required('student')
def student_attendance():
    db  = get_db()
    sid = session['user_id']
    attendance = db.execute("""
        SELECT a.*,s.name as subject_name FROM attendance a JOIN subjects s ON s.id=a.subject_id
        WHERE a.student_id=? ORDER BY a.date DESC""",(sid,)).fetchall()
    subject_stats = db.execute("""
        SELECT s.name,COUNT(a.id) as total,
               SUM(CASE WHEN a.status='present' THEN 1 ELSE 0 END) as present
        FROM attendance a JOIN subjects s ON s.id=a.subject_id
        WHERE a.student_id=? GROUP BY s.id""",(sid,)).fetchall()
    db.close()
    return render_template('student/attendance.html', attendance=attendance, subject_stats=subject_stats)

@app.route('/student/results')
@role_required('student')
def student_results():
    db  = get_db()
    sid = session['user_id']
    results   = db.execute("""
        SELECT r.*,s.name as subject_name FROM results r JOIN subjects s ON s.id=r.subject_id
        WHERE r.student_id=? AND r.published=1 ORDER BY r.semester,s.name""",(sid,)).fetchall()
    semesters = db.execute("""
        SELECT semester,AVG(gpa) as avg_gpa,SUM(total_marks) as total
        FROM results WHERE student_id=? AND published=1 GROUP BY semester""",(sid,)).fetchall()
    db.close()
    return render_template('student/results.html', results=results, semesters=semesters)

@app.route('/student/notices')
@role_required('student')
def student_notices():
    db = get_db()
    notices = db.execute("""
        SELECT n.*,u.name as posted_by_name FROM notices n LEFT JOIN users u ON u.id=n.posted_by
        WHERE n.audience IN ('all','students') ORDER BY n.created_at DESC""").fetchall()
    db.close()
    return render_template('student/notices.html', notices=notices)

@app.route('/student/fees')
@role_required('student')
def student_fees():
    db  = get_db()
    sid = session['user_id']
    fees = db.execute("SELECT * FROM fees WHERE student_id=? ORDER BY semester",(sid,)).fetchall()
    payments = db.execute("""
        SELECT fp.*,f.semester FROM fee_payments fp JOIN fees f ON f.id=fp.fee_id
        WHERE f.student_id=? ORDER BY fp.payment_date DESC""",(sid,)).fetchall()
    db.close()
    return render_template('student/fees.html', fees=fees, payments=payments)

# ─── eSewa payment initiation ─────────────────────────────────────────────────
@app.route('/student/fees/esewa/init/<int:fid>')
@role_required('student')
def esewa_init(fid):
    db  = get_db()
    sid = session['user_id']
    fee = db.execute("SELECT * FROM fees WHERE id=? AND student_id=?",(fid,sid)).fetchone()
    if not fee:
        flash('Fee record not found.','error'); db.close()
        return redirect(url_for('student_fees'))
    amount_due = fee['total_fee'] - fee['paid_amount']
    if amount_due <= 0:
        flash('This fee is already fully paid.','info'); db.close()
        return redirect(url_for('student_fees'))
    txn_id = 'SHB-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    db.execute("INSERT INTO esewa_transactions (fee_id,student_id,amount,transaction_id,status) VALUES (?,?,?,?,?)",
               (fid, sid, amount_due, txn_id, 'pending'))
    db.commit()
    db.close()
    # In production, redirect to eSewa payment gateway with proper params.
    # For demo, we redirect to a confirmation page.
    return render_template('student/esewa_pay.html', fee=fee,
                           amount_due=amount_due, txn_id=txn_id)

@app.route('/student/fees/esewa/success', methods=['GET','POST'])
@role_required('student')
def esewa_success():
    """Called after successful eSewa payment (simulated)."""
    db     = get_db()
    sid    = session['user_id']
    txn_id = request.args.get('oid') or request.form.get('oid','')
    ref_id = request.args.get('refId') or request.form.get('refId', 'SIM-' + ''.join(random.choices(string.digits,k=8)))
    amount = float(request.args.get('amt') or request.form.get('amt', 0))
    txn    = db.execute("SELECT * FROM esewa_transactions WHERE transaction_id=? AND student_id=?",
                         (txn_id, sid)).fetchone()
    if txn and txn['status'] == 'pending':
        db.execute("UPDATE esewa_transactions SET status='completed',ref_id=? WHERE id=?",(ref_id,txn['id']))
        fee      = db.execute("SELECT * FROM fees WHERE id=?",(txn['fee_id'],)).fetchone()
        new_paid = fee['paid_amount'] + txn['amount']
        status   = 'paid' if new_paid >= fee['total_fee'] else 'partial'
        db.execute("UPDATE fees SET paid_amount=?,status=? WHERE id=?",(new_paid,status,fee['id']))
        receipt  = 'ESW-' + ''.join(random.choices(string.digits,k=8))
        db.execute("INSERT INTO fee_payments (fee_id,amount,method,receipt_no,transaction_id) VALUES (?,?,?,?,?)",
                   (fee['id'], txn['amount'], 'esewa', receipt, ref_id))
        push_notification(db, sid, 'fee', 'Payment Successful',
                          f'eSewa payment of Rs {txn["amount"]:,.0f} confirmed. Receipt: {receipt}',
                          '/student/fees')
        db.commit()
        flash(f'eSewa payment successful! Receipt: {receipt}', 'success')
    else:
        flash('Payment verification failed or already processed.', 'error')
    db.close()
    return redirect(url_for('student_fees'))

@app.route('/student/fees/esewa/failure')
@role_required('student')
def esewa_failure():
    txn_id = request.args.get('oid','')
    db     = get_db()
    db.execute("UPDATE esewa_transactions SET status='failed' WHERE transaction_id=?",(txn_id,))
    db.commit(); db.close()
    flash('eSewa payment failed or was cancelled. Please try again.','error')
    return redirect(url_for('student_fees'))

@app.route('/student/timetable')
@role_required('student')
def student_timetable():
    db  = get_db()
    sid = session['user_id']
    class_info = db.execute("""
        SELECT c.* FROM classes c JOIN student_classes sc ON sc.class_id=c.id
        WHERE sc.student_id=?""",(sid,)).fetchone()
    timetable = []
    if class_info:
        timetable = db.execute("""
            SELECT t.*,s.name as subject_name,u.name as teacher_name FROM timetable t
            JOIN subjects s ON s.id=t.subject_id LEFT JOIN users u ON u.id=s.teacher_id
            WHERE t.class_id=? ORDER BY
            CASE t.day WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 ELSE 6 END, t.start_time""",
            (class_info['id'],)).fetchall()
    db.close()
    return render_template('student/timetable.html', timetable=timetable, class_info=class_info)

@app.route('/student/tasks')
@role_required('student')
def student_tasks():
    db  = get_db()
    sid = session['user_id']
    class_info = db.execute("""
        SELECT c.* FROM classes c JOIN student_classes sc ON sc.class_id=c.id
        WHERE sc.student_id=?""",(sid,)).fetchone()
    assignments = []
    if class_info:
        assignments = db.execute("""
            SELECT a.*,s.name as subject_name,s.id as subject_id,
                   sub.id as submission_id,sub.marks,sub.submitted_at
            FROM assignments a JOIN subjects s ON s.id=a.subject_id
            LEFT JOIN submissions sub ON sub.assignment_id=a.id AND sub.student_id=?
            WHERE s.class_id=? ORDER BY a.due_date""",(sid, class_info['id'])).fetchall()
    db.close()
    return render_template('student/tasks.html', assignments=assignments)

@app.route('/student/profile')
@role_required('student')
def student_profile():
    db   = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?",(session['user_id'],)).fetchone()
    db.close()
    return render_template('student/profile.html', user=user)

@app.route('/student/profile/update', methods=['POST'])
@role_required('student')
def student_update_profile():
    db  = get_db()
    sid = session['user_id']
    db.execute("UPDATE users SET name=?,phone=?,address=? WHERE id=?",
               (request.form['name'], request.form.get('phone'), request.form.get('address'), sid))
    db.commit(); db.close()
    session['name'] = request.form['name']
    flash('Profile updated!','success')
    return redirect(url_for('student_profile'))

# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/api/stats')
@login_required
def api_stats():
    db = get_db()
    d  = {
        'students': db.execute("SELECT COUNT(*) as c FROM users WHERE role='student'").fetchone()['c'],
        'teachers': db.execute("SELECT COUNT(*) as c FROM users WHERE role='teacher'").fetchone()['c'],
        'subjects': db.execute("SELECT COUNT(*) as c FROM subjects").fetchone()['c'],
    }
    db.close()
    return jsonify(d)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
=======
from app import create_app

app = create_app()

# For Vercel
if __name__ != '__main__':
    # Production mode for Vercel
    app.config['DEBUG'] = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> 3c7f15ec2d0064ebedc890ff39720893f503f309
