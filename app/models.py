from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False) # 'admin', 'teacher', 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIPS: These allow you to access profile info easily
    # uselist=False makes it a 1-to-1 relationship
    # cascade="all, delete-orphan" means if User is deleted, these are deleted too
    student_profile = db.relationship('Student', backref='user_account', cascade='all, delete-orphan', uselist=False)
    teacher_profile = db.relationship('Teacher', backref='user_account', cascade='all, delete-orphan', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id_no = db.Column(db.String(20), unique=True, nullable=False)
    year = db.Column(db.String(10))
    semester = db.Column(db.String(10))
    
    # Links to other data
    enrollments = db.relationship('Enrollment', backref='student', cascade='all, delete-orphan')
    attendance = db.relationship('Attendance', backref='student', cascade='all, delete-orphan')
    grades = db.relationship('Grade', backref='student', cascade='all, delete-orphan')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(100))
    
    # A teacher can teach many courses
    courses = db.relationship('Course', backref='instructor', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    
    enrollments = db.relationship('Enrollment', backref='course', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='course', cascade='all, delete-orphan')
    attendance = db.relationship('Attendance', backref='course', cascade='all, delete-orphan')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(10)) # Present/Absent

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime)
    file_path = db.Column(db.String(200))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    marks = db.Column(db.Float)
    total = db.Column(db.Float)