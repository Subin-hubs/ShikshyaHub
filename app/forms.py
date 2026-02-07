from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class AdminUserCreateForm(FlaskForm):
    # Basic User Info
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Temporary Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Account Role', choices=[('student', 'Student'), ('teacher', 'Teacher')], validators=[DataRequired()])
    
    # Specific ID numbers (used for student_id_no or employee_id)
    id_number = StringField('ID Number (College/Employee ID)', validators=[DataRequired()])
    
    # Student specific fields
    year = StringField('Year (e.g., 1st Year)')
    semester = StringField('Semester (e.g., 2nd Sem)')
    
    # Teacher specific fields
    department = StringField('Department (e.g., CS, Science)')
    
    submit = SubmitField('Create User ID')

    # Custom validation to check if email is already taken
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered in ShikshyaHub.')

class CourseCreateForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    code = StringField('Subject Code (e.g., CS101)', validators=[DataRequired(), Length(min=2, max=20)])
    
    # This will be populated with Teacher names in the route
    teacher_id = SelectField('Assign Teacher', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Generate Subject')