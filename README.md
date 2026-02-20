# ShikshyaHub 🎓
### Nepal's Professional Student Portal System

A complete, full-stack educational management system built with Flask, SQLite, and modern HTML/CSS/JS.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation & Run

```bash
# Clone / extract the project
cd ShikshyaHub

# Install dependencies
pip install -r requirements.txt

# OR run setup script (handles everything)
python setup.py

# OR manually:
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🔐 Demo Credentials

| Role    | Email                          | Password     |
|---------|-------------------------------|--------------|
| Admin   | admin@shikshyahub.edu         | Admin@123    |
| Teacher | teacher@shikshyahub.edu       | Teacher@123  |
| Student | student@shikshyahub.edu       | Student@123  |

---

## 📁 Project Structure

```
ShikshyaHub/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── setup.py                  # Setup & initialization script
├── shikshyahub.db           # SQLite database (auto-created)
│
├── static/
│   ├── css/
│   │   ├── main.css         # Global portal styles
│   │   ├── landing.css      # Landing page styles
│   │   └── login.css        # Login page styles
│   └── js/
│       ├── main.js          # Portal JavaScript
│       └── landing.js       # Landing page JS
│
└── templates/
    ├── base.html             # Portal base layout
    ├── landing.html          # Landing page
    ├── login.html            # Login page
    ├── admin/               # Admin portal templates
    │   ├── dashboard.html
    │   ├── students.html
    │   ├── teachers.html
    │   ├── subjects.html
    │   ├── classes.html
    │   ├── attendance.html
    │   ├── assignments.html
    │   ├── results.html
    │   ├── notices.html
    │   ├── fees.html
    │   └── timetable.html
    ├── teacher/             # Teacher portal templates
    │   ├── dashboard.html
    │   ├── subjects.html
    │   ├── subject_detail.html
    │   ├── submissions.html
    │   ├── attendance.html
    │   ├── results.html
    │   └── notices.html
    └── student/             # Student portal templates
        ├── dashboard.html
        ├── subjects.html
        ├── subject_detail.html
        ├── tasks.html
        ├── attendance.html
        ├── results.html
        ├── timetable.html
        ├── notices.html
        ├── fees.html
        └── profile.html
```

---

## ✨ Features

### 🏠 Landing Page
- Professional navbar with smooth scrolling
- Hero section with stats counter animation
- About, Services, Courses, Contact, Support sections
- Responsive mobile design

### 🔐 Login Page
- Split layout: visual panel + form panel
- Demo credentials panel
- Password toggle visibility
- Terms & conditions checkbox

### 👑 Admin Portal
- Dashboard with live stats
- Student management (create/delete/assign)
- Teacher management
- Subject management
- Class & program management
- Timetable builder
- Attendance monitoring
- Assignment tracking
- Results approval & publishing
- Notice board management
- Fee management with payment recording

### 👨‍🏫 Teacher Portal
- Dashboard with today's schedule
- Subject detail pages with materials & assignments
- Attendance marking system
- Assignment grading with feedback
- Results management
- Notice posting

### 🎓 Student Portal
- Dashboard with attendance & fee overview
- Subject pages with assignment submission
- Task manager (all assignments view)
- Detailed attendance reports
- Published results with GPA
- Weekly timetable
- Notice board
- Fee status & payment history
- Profile editor + Resume builder

---

## 🎨 Design

- **Fonts**: Cormorant Garamond (display) + DM Sans (body)
- **Colors**: Navy `#0f1f3d` × Gold `#c4962a` × Slate
- **Layout**: Fixed sidebar + sticky topbar + responsive grid
- **Animations**: Canvas charts, count-up, scroll reveal
- **Mobile**: Fully responsive with sliding sidebar

---

## 🛠️ Tech Stack

| Layer    | Technology |
|----------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend  | Flask (Python) |
| Database | SQLite |
| Charts   | Custom Canvas API |
| Fonts    | Google Fonts |

---

## 📊 Database Schema

- `users` — Admin, Teacher, Student accounts
- `programs` — Academic programs (BCS, BBA, etc.)
- `classes` — Classes per program/semester
- `student_classes` — Student→Class enrollment
- `subjects` — Subjects with teacher assignment
- `materials` — Course materials
- `assignments` — Subject assignments
- `submissions` — Student submissions + grades
- `attendance` — Daily attendance records
- `results` — Semester results + GPA
- `notices` — Announcements
- `fees` — Fee records per student
- `fee_payments` — Payment transactions
- `timetable` — Weekly schedule
- `qr_sessions` — QR code attendance sessions

---

## 📝 License
Built for educational use. © 2024 ShikshyaHub.
