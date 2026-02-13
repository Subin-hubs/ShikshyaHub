from datetime import datetime, date

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login hook to load a user from the database."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Authentication user for all roles.

    Only admins can create new users. Students and teachers can only log in.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(
        db.String(20), nullable=False
    )  # 'admin', 'teacher', 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one profiles
    student_profile = db.relationship(
        "Student",
        backref="user_account",
        cascade="all, delete-orphan",
        uselist=False,
    )
    teacher_profile = db.relationship(
        "Teacher",
        backref="user_account",
        cascade="all, delete-orphan",
        uselist=False,
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    """Student profile linked to a User with role='student'."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)  # e.g. "BSc CS 1st Year"

    # Relationships
    results = db.relationship(
        "Result", backref="student", cascade="all, delete-orphan"
    )
    attendance_records = db.relationship(
        "Attendance", backref="student", cascade="all, delete-orphan"
    )
    fees = db.relationship(
        "Fee", backref="student", cascade="all, delete-orphan", uselist=False
    )


class Teacher(db.Model):
    """Teacher profile linked to a User with role='teacher'."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(120), nullable=False)

    courses = db.relationship("Course", backref="teacher", lazy=True)


class Course(db.Model):
    """Course taught by a teacher for a particular class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    class_name = db.Column(
        db.String(50), nullable=False
    )  # link to Student.class_name
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=True)

    assignments = db.relationship(
        "Assignment", backref="course", cascade="all, delete-orphan"
    )
    results = db.relationship(
        "Result", backref="course", cascade="all, delete-orphan"
    )
    attendance_records = db.relationship(
        "Attendance", backref="course", cascade="all, delete-orphan"
    )


class Assignment(db.Model):
    """Assignments given in a course."""

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)


class Result(db.Model):
    """Marks obtained by a student in a course."""

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    marks = db.Column(db.Float, nullable=False)


class Attendance(db.Model):
    """Attendance record for a student on a particular date (optionally per course)."""

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    status = db.Column(
        db.String(10), nullable=False
    )  # 'Present' or 'Absent'


class Routine(db.Model):
    """Class routine for a given day."""

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # e.g. "Monday"
    subject = db.Column(db.String(120), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=True)
    time = db.Column(db.String(50), nullable=False)  # e.g. "09:00 AM - 10:00 AM"


class Noticeboard(db.Model):
    """Notices posted by admins."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Fee(db.Model):
    """Fee record for a student."""

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, nullable=False, default=0.0)
    due_amount = db.Column(db.Float, nullable=False, default=0.0)

    @property
    def status(self) -> str:
        if self.due_amount <= 0:
            return "Paid"
        if self.paid_amount > 0:
            return "Partial"
        return "Unpaid"