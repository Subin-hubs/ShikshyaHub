# create_admin_templates.py - Run this to create all admin templates
import os

# Define the template directory
TEMPLATE_DIR = r"d:\ShikshyaHub\app\templates\admin"

# Create courses.html
courses_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Courses - Admin Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
        }
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 0;
            position: sticky;
            top: 0;
        }
        .sidebar .brand {
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        .sidebar .brand h4 {
            margin: 0;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .sidebar .nav-menu {
            padding: 20px 0;
        }
        .sidebar .nav-item {
            padding: 0;
        }
        .sidebar .nav-link {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
            cursor: pointer;
        }
        .sidebar .nav-link:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-left-color: white;
        }
        .sidebar .nav-link.active {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border-left-color: white;
        }
        .sidebar .nav-link i {
            width: 20px;
            text-align: center;
        }
        .topbar {
            background: white;
            padding: 15px 25px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .topbar-user {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .topbar-user .user-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .card {
            border: none;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-radius: 10px;
        }
        .card h4 {
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #2563eb;
        }
        .table {
            margin-bottom: 0;
        }
        .table thead {
            background-color: #2563eb;
            color: white;
        }
        .table thead th {
            border: none;
            font-weight: 600;
            padding: 15px;
        }
        .table tbody td {
            padding: 15px;
            vertical-align: middle;
        }
        .table tbody tr:hover {
            background-color: #f0f6ff;
        }
        .badge {
            font-size: 0.85rem;
            padding: 5px 10px;
        }
        .btn-sm {
            padding: 5px 12px;
            font-size: 0.85rem;
            cursor: pointer;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            border: none;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        .btn-danger {
            background: linear-gradient(135deg, #dc3545 0%, #a71d2a 100%);
            border: none;
        }
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
        }
        .main-content {
            padding: 25px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-header h2 {
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        .page-header p {
            color: #666;
            margin: 0;
        }
        .search-box {
            margin-bottom: 20px;
        }
        .search-box .form-control {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 10px 15px;
            transition: all 0.3s ease;
        }
        .search-box .form-control:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.15);
        }
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                left: -100%;
                transition: left 0.3s ease;
                z-index: 1000;
                width: 250px;
            }
            .sidebar.active {
                left: 0;
            }
            .main-content {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row g-0" style="min-height: 100vh;">
            <!-- SIDEBAR -->
            <nav class="col-md-2 sidebar d-none d-md-block">
                <div class="brand">
                    <h4><i class="fas fa-graduation-cap"></i> Admin</h4>
                </div>
                <div class="nav-menu">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a href="{{ url_for('admin.dashboard') }}" class="nav-link">
                                <i class="fas fa-chart-line"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.manage_users') }}" class="nav-link">
                                <i class="fas fa-users"></i> Users
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.courses') }}" class="nav-link active">
                                <i class="fas fa-book"></i> Courses
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.attendance') }}" class="nav-link">
                                <i class="fas fa-calendar-check"></i> Attendance
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.reports') }}" class="nav-link">
                                <i class="fas fa-file-alt"></i> Reports
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('auth.logout') }}" class="nav-link">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
            <!-- MAIN CONTENT -->
            <main class="col-md-10 ms-sm-auto col-lg-10">
                <!-- TOPBAR -->
                <div class="topbar">
                    <div>
                        <h5 class="mb-0" style="color: #333; font-weight: 600;">Welcome, {{ current_user.name }}</h5>
                    </div>
                    <div class="topbar-user">
                        <span style="color: #666;">{{ current_user.email }}</span>
                        <div class="user-avatar">{{ current_user.name[0].upper() }}</div>
                    </div>
                </div>
                <!-- PAGE CONTENT -->
                <div class="main-content">
                    <!-- PAGE HEADER -->
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <div>
                            <h2>Manage Courses</h2>
                            <p>View and manage all courses in the system</p>
                        </div>
                        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addCourseModal">
                            <i class="fas fa-plus"></i> Add New Course
                        </button>
                    </div>
                    <!-- SEARCH BOX -->
                    <div class="search-box">
                        <input type="text" class="form-control" id="searchInput"
                            placeholder="Search by course name or code...">
                    </div>
                    <!-- COURSES TABLE -->
                    <div class="card p-3">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle" id="coursesTable">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Course Name</th>
                                        <th>Course Code</th>
                                        <th>Instructor</th>
                                        <th>Students Enrolled</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% if courses %}
                                    {% for course in courses %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td><strong>{{ course.name }}</strong></td>
                                        <td>{{ course.code }}</td>
                                        <td>{{ course.teacher.name if course.teacher else 'Not Assigned' }}</td>
                                        <td><span class="badge bg-info">{{ course.enrollments|length }}</span></td>
                                        <td><span class="badge bg-success">Active</span></td>
                                        <td>
                                            <button class="btn btn-sm btn-primary edit-course" data-id="{{ course.id }}" title="Edit Course">
                                                <i class="fas fa-edit"></i> Edit
                                            </button>
                                            <button class="btn btn-sm btn-danger delete-course" data-id="{{ course.id }}" title="Delete Course">
                                                <i class="fas fa-trash"></i> Delete
                                            </button>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                    {% else %}
                                    <tr>
                                        <td colspan="7" class="text-center py-4">
                                            <p class="text-muted">No courses found in the system.</p>
                                        </td>
                                    </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    <!-- Add Course Modal -->
    <div class="modal fade" id="addCourseModal" tabindex="-1" aria-labelledby="addCourseLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="addCourseLabel">
                        <i class="fas fa-book-plus"></i> Add New Course
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="addCourseForm">
                        <div class="mb-3">
                            <label for="courseName" class="form-label">Course Name</label>
                            <input type="text" class="form-control" id="courseName" placeholder="Web Development" required>
                        </div>
                        <div class="mb-3">
                            <label for="courseCode" class="form-label">Course Code</label>
                            <input type="text" class="form-control" id="courseCode" placeholder="WD-101" required>
                        </div>
                        <div class="mb-3">
                            <label for="courseTeacher" class="form-label">Instructor</label>
                            <select class="form-control" id="courseTeacher">
                                <option value="">Select an instructor</option>
                                {% for teacher in courses %}
                                    {% if teacher.teacher %}
                                    <option value="{{ teacher.teacher.id }}">{{ teacher.teacher.name }}</option>
                                    {% endif %}
                                {% endfor %}
                            </select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="addCourseBtn">Add Course</button>
                </div>
            </div>
        </div>
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Search functionality
        document.getElementById('searchInput').addEventListener('keyup', function () {
            const searchValue = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('#coursesTable tbody tr');
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
        
        // Add Course Button Click Handler
        document.getElementById('addCourseBtn')?.addEventListener('click', function() {
            const name = document.getElementById('courseName').value;
            const code = document.getElementById('courseCode').value;
            const teacher_id = document.getElementById('courseTeacher').value;
            
            if (!name || !code) {
                alert('Please fill all required fields');
                return;
            }
            
            fetch('{{ url_for("admin.add_course") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    code: code,
                    teacher_id: teacher_id || null
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Course added successfully!');
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
        
        // Edit Course
        document.querySelectorAll('.edit-course').forEach(btn => {
            btn.addEventListener('click', function() {
                alert('Edit functionality coming soon!');
            });
        });
        
        // Delete Course
        document.querySelectorAll('.delete-course').forEach(btn => {
            btn.addEventListener('click', function() {
                if (confirm('Are you sure you want to delete this course?')) {
                    const courseId = this.getAttribute('data-id');
                    fetch('{{ url_for("admin.delete_course", course_id=0) }}'.replace('0', courseId), {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Course deleted successfully!');
                            location.reload();
                        } else {
                            alert('Error: ' + data.message);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            });
        });
        
        // Mobile sidebar toggle
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('active');
        }
    </script>
</body>
</html>'''

# Create attendance.html
attendance_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attendance - Admin Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
        }
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 0;
            position: sticky;
            top: 0;
        }
        .sidebar .brand {
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        .sidebar .brand h4 {
            margin: 0;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .sidebar .nav-menu {
            padding: 20px 0;
        }
        .sidebar .nav-item {
            padding: 0;
        }
        .sidebar .nav-link {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
            cursor: pointer;
        }
        .sidebar .nav-link:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-left-color: white;
        }
        .sidebar .nav-link.active {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border-left-color: white;
        }
        .sidebar .nav-link i {
            width: 20px;
            text-align: center;
        }
        .topbar {
            background: white;
            padding: 15px 25px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .topbar-user {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .topbar-user .user-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .card {
            border: none;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-radius: 10px;
        }
        .card h4 {
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #2563eb;
        }
        .table {
            margin-bottom: 0;
        }
        .table thead {
            background-color: #2563eb;
            color: white;
        }
        .table thead th {
            border: none;
            font-weight: 600;
            padding: 15px;
        }
        .table tbody td {
            padding: 15px;
            vertical-align: middle;
        }
        .table tbody tr:hover {
            background-color: #f0f6ff;
        }
        .badge {
            font-size: 0.85rem;
            padding: 5px 10px;
        }
        .btn-sm {
            padding: 5px 12px;
            font-size: 0.85rem;
            cursor: pointer;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            border: none;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        .main-content {
            padding: 25px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-header h2 {
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        .page-header p {
            color: #666;
            margin: 0;
        }
        .search-box {
            margin-bottom: 20px;
        }
        .search-box .form-control {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 10px 15px;
            transition: all 0.3s ease;
        }
        .search-box .form-control:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.15);
        }
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                left: -100%;
                transition: left 0.3s ease;
                z-index: 1000;
                width: 250px;
            }
            .sidebar.active {
                left: 0;
            }
            .main-content {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row g-0" style="min-height: 100vh;">
            <!-- SIDEBAR -->
            <nav class="col-md-2 sidebar d-none d-md-block">
                <div class="brand">
                    <h4><i class="fas fa-graduation-cap"></i> Admin</h4>
                </div>
                <div class="nav-menu">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a href="{{ url_for('admin.dashboard') }}" class="nav-link">
                                <i class="fas fa-chart-line"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.manage_users') }}" class="nav-link">
                                <i class="fas fa-users"></i> Users
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.courses') }}" class="nav-link">
                                <i class="fas fa-book"></i> Courses
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.attendance') }}" class="nav-link active">
                                <i class="fas fa-calendar-check"></i> Attendance
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.reports') }}" class="nav-link">
                                <i class="fas fa-file-alt"></i> Reports
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('auth.logout') }}" class="nav-link">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
            <!-- MAIN CONTENT -->
            <main class="col-md-10 ms-sm-auto col-lg-10">
                <!-- TOPBAR -->
                <div class="topbar">
                    <div>
                        <h5 class="mb-0" style="color: #333; font-weight: 600;">Welcome, {{ current_user.name }}</h5>
                    </div>
                    <div class="topbar-user">
                        <span style="color: #666;">{{ current_user.email }}</span>
                        <div class="user-avatar">{{ current_user.name[0].upper() }}</div>
                    </div>
                </div>
                <!-- PAGE CONTENT -->
                <div class="main-content">
                    <!-- PAGE HEADER -->
                    <div class="page-header">
                        <h2>Attendance Records</h2>
                        <p>View and manage student attendance</p>
                    </div>
                    <!-- SEARCH BOX -->
                    <div class="search-box">
                        <input type="text" class="form-control" id="searchInput"
                            placeholder="Search by student name or ID...">
                    </div>
                    <!-- ATTENDANCE TABLE -->
                    <div class="card p-3">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle" id="attendanceTable">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Student Name</th>
                                        <th>Course</th>
                                        <th>Date</th>
                                        <th>Status</th>
                                        <th>Remarks</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% if attendance %}
                                    {% for record in attendance %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td><strong>{{ record.student.user.name if record.student else 'N/A' }}</strong></td>
                                        <td>{{ record.course.name if record.course else 'N/A' }}</td>
                                        <td>{{ record.date.strftime('%b %d, %Y') if record.date else 'N/A' }}</td>
                                        <td>
                                            {% if record.status == 'present' %}
                                                <span class="badge bg-success">Present</span>
                                            {% elif record.status == 'absent' %}
                                                <span class="badge bg-danger">Absent</span>
                                            {% else %}
                                                <span class="badge bg-warning">Leave</span>
                                            {% endif %}
                                        </td>
                                        <td>{{ record.remarks or '-' }}</td>
                                        <td>
                                            <button class="btn btn-sm btn-primary edit-attendance" data-id="{{ record.id }}" title="Edit">
                                                <i class="fas fa-edit"></i> Edit
                                            </button>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                    {% else %}
                                    <tr>
                                        <td colspan="7" class="text-center py-4">
                                            <p class="text-muted">No attendance records found.</p>
                                        </td>
                                    </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Search functionality
        document.getElementById('searchInput').addEventListener('keyup', function () {
            const searchValue = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('#attendanceTable tbody tr');
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
        
        // Edit Attendance
        document.querySelectorAll('.edit-attendance').forEach(btn => {
            btn.addEventListener('click', function() {
                alert('Edit attendance functionality coming soon!');
            });
        });
        
        // Mobile sidebar toggle
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('active');
        }
    </script>
</body>
</html>'''

# Create reports.html
reports_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reports - Admin Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
        }
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 0;
            position: sticky;
            top: 0;
        }
        .sidebar .brand {
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        .sidebar .brand h4 {
            margin: 0;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .sidebar .nav-menu {
            padding: 20px 0;
        }
        .sidebar .nav-item {
            padding: 0;
        }
        .sidebar .nav-link {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
            cursor: pointer;
        }
        .sidebar .nav-link:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-left-color: white;
        }
        .sidebar .nav-link.active {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border-left-color: white;
        }
        .sidebar .nav-link i {
            width: 20px;
            text-align: center;
        }
        .topbar {
            background: white;
            padding: 15px 25px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .topbar-user {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .topbar-user .user-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .stat-card {
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: none;
            transition: all 0.3s ease;
            padding: 20px;
            color: white;
            text-align: center;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        .stat-card h5 {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .stat-card h3 {
            font-size: 2.5rem;
            font-weight: 700;
        }
        .stat-primary {
            background: linear-gradient(135deg, #0d6efd 0%, #0056b3 100%);
        }
        .stat-success {
            background: linear-gradient(135deg, #198754 0%, #0d5834 100%);
        }
        .stat-info {
            background: linear-gradient(135deg, #0dcaf0 0%, #0a8fab 100%);
        }
        .stat-warning {
            background: linear-gradient(135deg, #ffc107 0%, #d39e00 100%);
            color: #333;
        }
        .card {
            border: none;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-radius: 10px;
        }
        .card h4 {
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #2563eb;
        }
        .main-content {
            padding: 25px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-header h2 {
            font-weight: 700;
            color: #333;
            margin-bottom: 5px;
        }
        .page-header p {
            color: #666;
            margin: 0;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            border: none;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                left: -100%;
                transition: left 0.3s ease;
                z-index: 1000;
                width: 250px;
            }
            .sidebar.active {
                left: 0;
            }
            .main-content {
                padding: 15px;
            }
            .stat-card h3 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row g-0" style="min-height: 100vh;">
            <!-- SIDEBAR -->
            <nav class="col-md-2 sidebar d-none d-md-block">
                <div class="brand">
                    <h4><i class="fas fa-graduation-cap"></i> Admin</h4>
                </div>
                <div class="nav-menu">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a href="{{ url_for('admin.dashboard') }}" class="nav-link">
                                <i class="fas fa-chart-line"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.manage_users') }}" class="nav-link">
                                <i class="fas fa-users"></i> Users
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.courses') }}" class="nav-link">
                                <i class="fas fa-book"></i> Courses
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.attendance') }}" class="nav-link">
                                <i class="fas fa-calendar-check"></i> Attendance
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('admin.reports') }}" class="nav-link active">
                                <i class="fas fa-file-alt"></i> Reports
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{{ url_for('auth.logout') }}" class="nav-link">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
            <!-- MAIN CONTENT -->
            <main class="col-md-10 ms-sm-auto col-lg-10">
                <!-- TOPBAR -->
                <div class="topbar">
                    <div>
                        <h5 class="mb-0" style="color: #333; font-weight: 600;">Welcome, {{ current_user.name }}</h5>
                    </div>
                    <div class="topbar-user">
                        <span style="color: #666;">{{ current_user.email }}</span>
                        <div class="user-avatar">{{ current_user.name[0].upper() }}</div>
                    </div>
                </div>
                <!-- PAGE CONTENT -->
                <div class="main-content">
                    <!-- PAGE HEADER -->
                    <div class="page-header">
                        <h2>System Reports</h2>
                        <p>Generate and view system reports</p>
                    </div>
                    <!-- REPORT CARDS -->
                    <div class="row g-4 mb-4">
                        <div class="col-md-3">
                            <div class="card stat-card stat-primary">
                                <h5>Total Students</h5>
                                <h3>{{ students_count }}</h3>
                                <p class="small mt-2">Active students in the system</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card stat-card stat-success">
                                <h5>Total Teachers</h5>
                                <h3>{{ teachers_count }}</h3>
                                <p class="small mt-2">Registered instructors</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card stat-card stat-info">
                                <h5>Total Courses</h5>
                                <h3>{{ courses_count }}</h3>
                                <p class="small mt-2">Active courses</p>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card stat-card stat-warning">
                                <h5>Total Enrollments</h5>
                                <h3>{{ total_enrollments }}</h3>
                                <p class="small mt-2">Course enrollments</p>
                            </div>
                        </div>
                    </div>
                    <!-- REPORT OPTIONS -->
                    <div class="card p-4">
                        <h4>Generate Reports</h4>
                        <div class="row g-3">
                            <div class="col-md-4">
                                <button class="btn btn-primary w-100" onclick="generateStudentReport()">
                                    <i class="fas fa-download"></i> Student Report
                                </button>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-primary w-100" onclick="generateAttendanceReport()">
                                    <i class="fas fa-download"></i> Attendance Report
                                </button>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-primary w-100" onclick="generateCourseReport()">
                                    <i class="fas fa-download"></i> Course Report
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function generateStudentReport() {
            alert('Student Report generation in progress...');
            console.log('Generating student report...');
        }
        
        function generateAttendanceReport() {
            alert('Attendance Report generation in progress...');
            console.log('Generating attendance report...');
        }
        
        function generateCourseReport() {
            alert('Course Report generation in progress...');
            console.log('Generating course report...');
        }
        
        // Mobile sidebar toggle
        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('active');
        }
    </script>
</body>
</html>'''

# Write files
os.makedirs(TEMPLATE_DIR, exist_ok=True)

with open(os.path.join(TEMPLATE_DIR, 'courses.html'), 'w', encoding='utf-8') as f:
    f.write(courses_html)
    print("✅ Created courses.html")

with open(os.path.join(TEMPLATE_DIR, 'attendance.html'), 'w', encoding='utf-8') as f:
    f.write(attendance_html)
    print("✅ Created attendance.html")

with open(os.path.join(TEMPLATE_DIR, 'reports.html'), 'w', encoding='utf-8') as f:
    f.write(reports_html)
    print("✅ Created reports.html")

print("\n✅ All admin template files created successfully!")