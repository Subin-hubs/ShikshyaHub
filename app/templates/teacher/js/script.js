// ==========================================
// TEACHER PORTAL - MAIN JAVASCRIPT FILE
// ==========================================

// Dummy Teacher Data
const teacherData = {
  id: 'TCH001',
  name: 'Prof. Michael Anderson',
  email: 'michael.anderson@school.edu',
  subject: 'Computer Science',
  department: 'Technology',
  phone: '+1 (555) 987-6543',
  joinDate: '2019-09-01',
  qualification: 'Ph.D. in Computer Science',
  experience: '8 years'
};

// Dummy Students Data
const studentsData = [
  {
    id: 'STD001',
    name: 'Emma Wilson',
    email: 'emma.wilson@student.edu',
    grade: 'A',
    midterm: 88,
    final: 92,
    assignments: 95,
    total: 91.7,
    attendance: 95
  },
  {
    id: 'STD002',
    name: 'James Brown',
    email: 'james.brown@student.edu',
    grade: 'B+',
    midterm: 82,
    final: 85,
    assignments: 88,
    total: 85.0,
    attendance: 88
  },
  {
    id: 'STD003',
    name: 'Sophia Martinez',
    email: 'sophia.martinez@student.edu',
    grade: 'A+',
    midterm: 95,
    final: 98,
    assignments: 100,
    total: 97.7,
    attendance: 100
  },
  {
    id: 'STD004',
    name: 'Oliver Johnson',
    email: 'oliver.johnson@student.edu',
    grade: 'B',
    midterm: 75,
    final: 78,
    assignments: 82,
    total: 78.3,
    attendance: 85
  },
  {
    id: 'STD005',
    name: 'Ava Davis',
    email: 'ava.davis@student.edu',
    grade: 'A',
    midterm: 90,
    final: 91,
    assignments: 93,
    total: 91.3,
    attendance: 92
  },
  {
    id: 'STD006',
    name: 'William Garcia',
    email: 'william.garcia@student.edu',
    grade: 'B+',
    midterm: 84,
    final: 86,
    assignments: 89,
    total: 86.3,
    attendance: 90
  },
  {
    id: 'STD007',
    name: 'Isabella Rodriguez',
    email: 'isabella.rodriguez@student.edu',
    grade: 'A',
    midterm: 87,
    final: 89,
    assignments: 91,
    total: 89.0,
    attendance: 93
  },
  {
    id: 'STD008',
    name: 'Lucas Lee',
    email: 'lucas.lee@student.edu',
    grade: 'C+',
    midterm: 70,
    final: 72,
    assignments: 75,
    total: 72.3,
    attendance: 78
  }
];

// Dummy Course Materials Data
const courseMaterials = [
  {
    id: 'MAT001',
    title: 'Introduction to Programming - Lecture Notes',
    type: 'PDF',
    uploadDate: '2026-01-15',
    size: '2.5 MB',
    downloads: 42
  },
  {
    id: 'MAT002',
    title: 'Data Structures - Presentation Slides',
    type: 'PPTX',
    uploadDate: '2026-01-20',
    size: '5.8 MB',
    downloads: 38
  },
  {
    id: 'MAT003',
    title: 'Algorithm Analysis - Video Lecture',
    type: 'MP4',
    uploadDate: '2026-02-01',
    size: '125 MB',
    downloads: 35
  },
  {
    id: 'MAT004',
    title: 'Practice Problems - Chapter 5',
    type: 'PDF',
    uploadDate: '2026-02-05',
    size: '1.2 MB',
    downloads: 40
  }
];

// Dummy Assignments Data
const assignmentsData = [
  {
    id: 'ASG001',
    title: 'Binary Search Tree Implementation',
    description: 'Implement a balanced BST with insert, delete, and search operations in Python',
    dueDate: '2026-02-20',
    uploadDate: '2026-02-05',
    totalSubmissions: 6,
    totalStudents: 8,
    status: 'active'
  },
  {
    id: 'ASG002',
    title: 'Sorting Algorithm Analysis',
    description: 'Compare time complexity of QuickSort, MergeSort, and HeapSort with detailed report',
    dueDate: '2026-02-15',
    uploadDate: '2026-01-28',
    totalSubmissions: 8,
    totalStudents: 8,
    status: 'completed'
  },
  {
    id: 'ASG003',
    title: 'Graph Traversal Project',
    description: 'Implement BFS and DFS algorithms and apply to real-world problem',
    dueDate: '2026-02-25',
    uploadDate: '2026-02-10',
    totalSubmissions: 3,
    totalStudents: 8,
    status: 'active'
  },
  {
    id: 'ASG004',
    title: 'Database Design Assignment',
    description: 'Design and normalize a database schema for a library management system',
    dueDate: '2026-02-12',
    uploadDate: '2026-01-25',
    totalSubmissions: 8,
    totalStudents: 8,
    status: 'graded'
  }
];

// Dummy Routine Data
const routineData = {
  Monday: [
    { time: '9:00 AM - 10:00 AM', subject: 'Computer Science', room: 'Room 301', type: 'Lecture' },
    { time: '11:00 AM - 12:00 PM', subject: 'Computer Science', room: 'Lab 2', type: 'Lab' }
  ],
  Tuesday: [
    { time: '10:00 AM - 11:00 AM', subject: 'Computer Science', room: 'Room 301', type: 'Lecture' },
    { time: '2:00 PM - 3:00 PM', subject: 'Office Hours', room: 'Office 205', type: 'Consultation' }
  ],
  Wednesday: [
    { time: '9:00 AM - 10:00 AM', subject: 'Computer Science', room: 'Room 301', type: 'Lecture' },
    { time: '11:00 AM - 12:00 PM', subject: 'Computer Science', room: 'Lab 2', type: 'Lab' }
  ],
  Thursday: [
    { time: '10:00 AM - 11:00 AM', subject: 'Computer Science', room: 'Room 301', type: 'Lecture' },
    { time: '3:00 PM - 4:00 PM', subject: 'Faculty Meeting', room: 'Conference Room', type: 'Meeting' }
  ],
  Friday: [
    { time: '9:00 AM - 10:00 AM', subject: 'Computer Science', room: 'Room 301', type: 'Tutorial' },
    { time: '2:00 PM - 3:00 PM', subject: 'Office Hours', room: 'Office 205', type: 'Consultation' }
  ]
};

// Dummy Notices Data
const noticesData = [
  {
    id: 'NOT001',
    title: 'Mid-Semester Examination Schedule',
    content: 'The mid-semester exam for Computer Science will be held on March 5, 2026. Topics covered: Chapters 1-5. Duration: 2 hours. Room: Hall A.',
    date: '2026-02-10',
    urgent: true
  },
  {
    id: 'NOT002',
    title: 'Assignment Deadline Extension',
    content: 'The deadline for Assignment ASG001 has been extended to February 22, 2026 due to technical issues with the submission portal.',
    date: '2026-02-12',
    urgent: false
  },
  {
    id: 'NOT003',
    title: 'Guest Lecture on Machine Learning',
    content: 'We will have a guest lecture by Dr. Sarah Chen from MIT on February 18, 2026 at 3:00 PM. Attendance is mandatory.',
    date: '2026-02-08',
    urgent: true
  },
  {
    id: 'NOT004',
    title: 'Lab Session Rescheduled',
    content: 'Wednesday lab session is rescheduled to Thursday 2:00 PM this week only. Please adjust your schedule accordingly.',
    date: '2026-02-06',
    urgent: false
  }
];

// Attendance tracking
let attendanceRecords = studentsData.map(student => ({
  studentId: student.id,
  studentName: student.name,
  present: Math.floor(student.attendance * 0.4), // Approximate number of classes attended
  absent: Math.floor((100 - student.attendance) * 0.4),
  percentage: student.attendance
}));

// ==========================================
// NAVIGATION FUNCTIONS
// ==========================================

// Set active sidebar link based on current page
function setActiveSidebarLink() {
  const currentPage = window.location.pathname.split('/').pop();
  const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
  
  sidebarLinks.forEach(link => {
    link.classList.remove('active');
    const href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });
}

// Mobile sidebar toggle
function initMobileSidebar() {
  const toggleBtn = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 968) {
        if (!e.target.closest('.sidebar') && !e.target.closest('.sidebar-toggle')) {
          sidebar.classList.remove('active');
        }
      }
    });
  }
}

// ==========================================
// LOGOUT FUNCTIONALITY
// ==========================================

function initLogout() {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
}

function handleLogout() {
  const confirmed = confirm('Are you sure you want to logout?');
  if (confirmed) {
    localStorage.clear();
    sessionStorage.clear();
    alert('Logged out successfully!');
    window.location.href = 'teacher_dashboard.html';
  }
}

// ==========================================
// DASHBOARD FUNCTIONS
// ==========================================

function loadDashboard() {
  loadTeacherInfo();
  loadDashboardStats();
  loadRecentActivity();
}

function loadTeacherInfo() {
  const teacherInfoDiv = document.getElementById('teacher-info');
  if (!teacherInfoDiv) return;
  
  teacherInfoDiv.innerHTML = `
    <div class="profile-header">
      <div class="profile-avatar">${teacherData.name.split(' ').map(n => n[0]).join('')}</div>
      <div class="profile-details">
        <h2>Welcome, ${teacherData.name}!</h2>
        <p>${teacherData.qualification} • ${teacherData.subject} Teacher</p>
      </div>
    </div>
  `;
}

function loadDashboardStats() {
  const statsDiv = document.getElementById('teacher-stats');
  if (!statsDiv) return;
  
  const totalStudents = studentsData.length;
  const totalAssignments = assignmentsData.length;
  const avgAttendance = (studentsData.reduce((sum, s) => sum + s.attendance, 0) / studentsData.length).toFixed(1);
  const totalNotices = noticesData.length;
  
  statsDiv.innerHTML = `
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-card-header">
          <div>
            <div class="stat-value">${totalStudents}</div>
            <div class="stat-label">Total Students</div>
          </div>
          <div class="stat-icon">👨‍🎓</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-card-header">
          <div>
            <div class="stat-value">${totalAssignments}</div>
            <div class="stat-label">Assignments Uploaded</div>
          </div>
          <div class="stat-icon">📚</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-card-header">
          <div>
            <div class="stat-value">${avgAttendance}%</div>
            <div class="stat-label">Attendance Overview</div>
          </div>
          <div class="stat-icon">✓</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-card-header">
          <div>
            <div class="stat-value">${totalNotices}</div>
            <div class="stat-label">Notices Posted</div>
          </div>
          <div class="stat-icon">📢</div>
        </div>
      </div>
    </div>
  `;
}

function loadRecentActivity() {
  const activityDiv = document.getElementById('recent-activity');
  if (!activityDiv) return;
  
  let html = '<div class="card"><div class="card-header"><h2 class="card-title">Recent Activity</h2></div>';
  
  const recentActivities = [
    { type: 'assignment', text: '3 new submissions for "Graph Traversal Project"', time: '2 hours ago' },
    { type: 'notice', text: 'Posted notice about exam schedule', time: '5 hours ago' },
    { type: 'material', text: 'Uploaded "Practice Problems - Chapter 5"', time: '1 day ago' },
    { type: 'grade', text: 'Graded "Database Design Assignment" for 8 students', time: '2 days ago' },
    { type: 'attendance', text: 'Marked attendance for Monday class', time: '3 days ago' }
  ];
  
  recentActivities.forEach(activity => {
    const icon = activity.type === 'assignment' ? '📝' :
                 activity.type === 'notice' ? '📢' :
                 activity.type === 'material' ? '📚' :
                 activity.type === 'grade' ? '✓' : '👥';
    
    html += `
      <div class="list-item">
        <div class="list-item-header">
          <div>
            <div class="list-item-title">${icon} ${activity.text}</div>
            <div class="list-item-meta">${activity.time}</div>
          </div>
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  activityDiv.innerHTML = html;
}

// ==========================================
// ROUTINE FUNCTIONS
// ==========================================

function loadRoutine() {
  const routineTableDiv = document.getElementById('routine-table');
  if (!routineTableDiv) return;
  
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  
  let html = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Weekly Class Schedule</h2>
      </div>
      <div class="table-container">
        <table class="routine-table">
          <thead>
            <tr>
              <th>Day</th>
              <th>Time</th>
              <th>Subject/Activity</th>
              <th>Room</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  days.forEach(day => {
    const classes = routineData[day] || [];
    if (classes.length === 0) {
      html += `
        <tr>
          <td class="time-cell">${day}</td>
          <td colspan="4" style="text-align: center; color: var(--text-muted);">No classes scheduled</td>
        </tr>
      `;
    } else {
      classes.forEach((classInfo, index) => {
        html += `
          <tr>
            ${index === 0 ? `<td class="time-cell" rowspan="${classes.length}">${day}</td>` : ''}
            <td>${classInfo.time}</td>
            <td>${classInfo.subject}</td>
            <td>${classInfo.room}</td>
            <td><span class="badge badge-primary">${classInfo.type}</span></td>
          </tr>
        `;
      });
    }
  });
  
  html += '</tbody></table></div></div>';
  routineTableDiv.innerHTML = html;
}

// ==========================================
// COURSE MATERIALS FUNCTIONS
// ==========================================

function loadCourseMaterials() {
  const materialsDiv = document.getElementById('course-materials');
  if (!materialsDiv) return;
  
  let html = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Uploaded Course Materials</h2>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Type</th>
              <th>Upload Date</th>
              <th>Size</th>
              <th>Downloads</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  courseMaterials.forEach(material => {
    html += `
      <tr>
        <td>${material.title}</td>
        <td><span class="badge badge-info">${material.type}</span></td>
        <td>${new Date(material.uploadDate).toLocaleDateString()}</td>
        <td>${material.size}</td>
        <td>${material.downloads}</td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="deleteMaterial('${material.id}')">Delete</button>
        </td>
      </tr>
    `;
  });
  
  html += '</tbody></table></div></div>';
  materialsDiv.innerHTML = html;
}

function initUploadForm() {
  const uploadFormDiv = document.getElementById('upload-form');
  if (!uploadFormDiv) return;
  
  uploadFormDiv.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Upload New Material</h2>
      </div>
      <form onsubmit="handleMaterialUpload(event)">
        <div class="form-group">
          <label class="form-label">Material Title</label>
          <input type="text" class="form-input" placeholder="e.g., Chapter 5 - Lecture Notes" required>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Material Type</label>
            <select class="form-select" required>
              <option value="">Select Type</option>
              <option value="PDF">PDF Document</option>
              <option value="PPTX">PowerPoint Presentation</option>
              <option value="MP4">Video Lecture</option>
              <option value="ZIP">Compressed File</option>
              <option value="DOCX">Word Document</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">File</label>
            <input type="file" class="form-input" required>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Upload Material</button>
      </form>
    </div>
  `;
}

function handleMaterialUpload(e) {
  e.preventDefault();
  alert('Course material uploaded successfully!');
  e.target.reset();
}

function deleteMaterial(materialId) {
  if (confirm('Are you sure you want to delete this material?')) {
    alert(`Material ${materialId} deleted successfully!`);
  }
}

// ==========================================
// ASSIGNMENTS FUNCTIONS
// ==========================================

function loadAssignments() {
  const assignmentsTableDiv = document.getElementById('assignments-table');
  if (!assignmentsTableDiv) return;
  
  let html = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">All Assignments</h2>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Assignment Title</th>
              <th>Due Date</th>
              <th>Submissions</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  assignmentsData.forEach(assignment => {
    const submissionRate = ((assignment.totalSubmissions / assignment.totalStudents) * 100).toFixed(0);
    const statusBadge = assignment.status === 'active' ? 'badge-primary' :
                       assignment.status === 'completed' ? 'badge-success' : 'badge-info';
    
    html += `
      <tr>
        <td>
          <strong>${assignment.title}</strong>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">${assignment.description}</div>
        </td>
        <td>${new Date(assignment.dueDate).toLocaleDateString()}</td>
        <td>${assignment.totalSubmissions}/${assignment.totalStudents} (${submissionRate}%)</td>
        <td><span class="badge ${statusBadge}">${assignment.status}</span></td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="viewSubmissions('${assignment.id}')">View</button>
          <button class="btn btn-sm btn-danger" onclick="deleteAssignment('${assignment.id}')">Delete</button>
        </td>
      </tr>
    `;
  });
  
  html += '</tbody></table></div></div>';
  assignmentsTableDiv.innerHTML = html;
}

function initAssignmentUploadForm() {
  const uploadFormDiv = document.getElementById('upload-assignment-form');
  if (!uploadFormDiv) return;
  
  uploadFormDiv.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Upload New Assignment</h2>
      </div>
      <form onsubmit="handleAssignmentUpload(event)">
        <div class="form-group">
          <label class="form-label">Assignment Title</label>
          <input type="text" class="form-input" placeholder="e.g., Binary Tree Implementation" required>
        </div>
        <div class="form-group">
          <label class="form-label">Description</label>
          <textarea class="form-textarea" placeholder="Enter assignment description and requirements" required></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Due Date</label>
            <input type="date" class="form-input" required>
          </div>
          <div class="form-group">
            <label class="form-label">Assignment File (Optional)</label>
            <input type="file" class="form-input">
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Upload Assignment</button>
      </form>
    </div>
  `;
}

function handleAssignmentUpload(e) {
  e.preventDefault();
  alert('Assignment uploaded successfully!');
  e.target.reset();
}

function viewSubmissions(assignmentId) {
  alert(`Viewing submissions for assignment: ${assignmentId}`);
}

function deleteAssignment(assignmentId) {
  if (confirm('Are you sure you want to delete this assignment?')) {
    alert(`Assignment ${assignmentId} deleted successfully!`);
  }
}

// ==========================================
// RESULTS FUNCTIONS
// ==========================================

function loadResults() {
  loadResultsTable();
  loadResultsSummary();
}

function loadResultsTable() {
  const resultsTableDiv = document.getElementById('results-table');
  if (!resultsTableDiv) return;
  
  let html = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Student Results</h2>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Student Name</th>
              <th>Midterm</th>
              <th>Final</th>
              <th>Assignments</th>
              <th>Total</th>
              <th>Grade</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  studentsData.forEach(student => {
    const gradeBadge = student.grade.includes('A') ? 'badge-success' :
                      student.grade.includes('B') ? 'badge-primary' :
                      student.grade.includes('C') ? 'badge-warning' : 'badge-danger';
    
    html += `
      <tr>
        <td>${student.name}</td>
        <td>${student.midterm}</td>
        <td>${student.final}</td>
        <td>${student.assignments}</td>
        <td><strong>${student.total}</strong></td>
        <td><span class="badge ${gradeBadge}">${student.grade}</span></td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="editGrade('${student.id}')">Edit</button>
        </td>
      </tr>
    `;
  });
  
  html += '</tbody></table></div></div>';
  resultsTableDiv.innerHTML = html;
}

function loadResultsSummary() {
  const summaryDiv = document.getElementById('results-summary');
  if (!summaryDiv) return;
  
  const avgTotal = (studentsData.reduce((sum, s) => sum + s.total, 0) / studentsData.length).toFixed(1);
  const gradeCount = studentsData.reduce((acc, s) => {
    const grade = s.grade.charAt(0);
    acc[grade] = (acc[grade] || 0) + 1;
    return acc;
  }, {});
  
  summaryDiv.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Results Summary</h2>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">${avgTotal}%</div>
          <div class="stat-label">Class Average</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${gradeCount['A'] || 0}</div>
          <div class="stat-label">A Grades</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${gradeCount['B'] || 0}</div>
          <div class="stat-label">B Grades</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${gradeCount['C'] || 0}</div>
          <div class="stat-label">C Grades</div>
        </div>
      </div>
    </div>
  `;
}

function editGrade(studentId) {
  alert(`Editing grade for student: ${studentId}`);
}

// ==========================================
// ATTENDANCE FUNCTIONS
// ==========================================

function loadAttendance() {
  const attendanceTableDiv = document.getElementById('attendance-table');
  if (!attendanceTableDiv) return;
  
  let html = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Student Attendance</h2>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Student Name</th>
              <th>Present</th>
              <th>Absent</th>
              <th>Total Classes</th>
              <th>Percentage</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
  `;
  
  attendanceRecords.forEach(record => {
    const total = record.present + record.absent;
    const statusBadge = record.percentage >= 90 ? 'badge-success' :
                       record.percentage >= 75 ? 'badge-primary' :
                       record.percentage >= 60 ? 'badge-warning' : 'badge-danger';
    const statusText = record.percentage >= 75 ? 'Good' : 'Low';
    
    html += `
      <tr>
        <td>${record.studentName}</td>
        <td>${record.present}</td>
        <td>${record.absent}</td>
        <td>${total}</td>
        <td><strong>${record.percentage}%</strong></td>
        <td><span class="badge ${statusBadge}">${statusText}</span></td>
      </tr>
    `;
  });
  
  html += '</tbody></table></div></div>';
  attendanceTableDiv.innerHTML = html;
}

function initAttendanceForm() {
  const attendanceFormDiv = document.getElementById('attendance-form');
  if (!attendanceFormDiv) return;
  
  attendanceFormDiv.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Mark Today's Attendance</h2>
      </div>
      <form onsubmit="handleAttendanceSubmit(event)">
        <div class="form-group">
          <label class="form-label">Date</label>
          <input type="date" class="form-input" value="${new Date().toISOString().split('T')[0]}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Select Present Students</label>
          <div style="max-height: 300px; overflow-y: auto; border: 2px solid var(--border); border-radius: 8px; padding: 1rem; background: var(--bg-card);">
            ${studentsData.map(student => `
              <label style="display: block; padding: 0.5rem; cursor: pointer; transition: background 0.2s;">
                <input type="checkbox" style="margin-right: 0.5rem;" value="${student.id}" checked>
                ${student.name}
              </label>
            `).join('')}
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Submit Attendance</button>
      </form>
    </div>
  `;
}

function handleAttendanceSubmit(e) {
  e.preventDefault();
  alert('Attendance marked successfully!');
}

// ==========================================
// NOTICEBOARD FUNCTIONS
// ==========================================

function loadNotices() {
  const noticeListDiv = document.getElementById('notice-list');
  if (!noticeListDiv) return;
  
  let html = '<div class="card"><div class="card-header"><h2 class="card-title">All Notices</h2></div>';
  
  const sortedNotices = [...noticesData].sort((a, b) => new Date(b.date) - new Date(a.date));
  
  sortedNotices.forEach(notice => {
    const urgentBadge = notice.urgent ? '<span class="badge badge-danger">Urgent</span>' : '';
    const urgentStyle = notice.urgent ? 'border-left: 4px solid var(--danger);' : '';
    
    html += `
      <div class="list-item" style="${urgentStyle}">
        <div class="list-item-header">
          <div>
            <div class="list-item-title">${notice.title}</div>
            <div class="list-item-meta">Posted on ${new Date(notice.date).toLocaleDateString()}</div>
          </div>
          ${urgentBadge}
        </div>
        <div class="list-item-content">${notice.content}</div>
        <div class="list-item-actions">
          <button class="btn btn-sm btn-outline" onclick="editNotice('${notice.id}')">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="deleteNotice('${notice.id}')">Delete</button>
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  noticeListDiv.innerHTML = html;
}

function initNoticeForm() {
  const noticeFormDiv = document.getElementById('notice-form');
  if (!noticeFormDiv) return;
  
  noticeFormDiv.innerHTML = `
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Post New Notice</h2>
      </div>
      <form onsubmit="handleNoticeSubmit(event)">
        <div class="form-group">
          <label class="form-label">Notice Title</label>
          <input type="text" class="form-input" placeholder="Enter notice title" required>
        </div>
        <div class="form-group">
          <label class="form-label">Content</label>
          <textarea class="form-textarea" placeholder="Enter notice content" required></textarea>
        </div>
        <div class="form-group">
          <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
            <input type="checkbox" id="urgent-checkbox">
            <span class="form-label" style="margin: 0;">Mark as Urgent</span>
          </label>
        </div>
        <button type="submit" class="btn btn-primary">Post Notice</button>
      </form>
    </div>
  `;
}

function handleNoticeSubmit(e) {
  e.preventDefault();
  alert('Notice posted successfully!');
  e.target.reset();
}

function editNotice(noticeId) {
  alert(`Editing notice: ${noticeId}`);
}

function deleteNotice(noticeId) {
  if (confirm('Are you sure you want to delete this notice?')) {
    alert(`Notice ${noticeId} deleted successfully!`);
  }
}

// ==========================================
// PROFILE FUNCTIONS
// ==========================================

function loadProfile() {
  const profileInfoDiv = document.getElementById('profile-info');
  if (!profileInfoDiv) return;
  
  profileInfoDiv.innerHTML = `
    <div class="profile-header">
      <div class="profile-avatar">${teacherData.name.split(' ').map(n => n[0]).join('')}</div>
      <div class="profile-details">
        <h2>${teacherData.name}</h2>
        <p>${teacherData.subject} Teacher • ${teacherData.department} Department</p>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Personal Information</h2>
        <button class="btn btn-outline" onclick="toggleEditProfile()">Edit Profile</button>
      </div>
      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">Teacher ID</div>
          <div class="info-value">${teacherData.id}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Email</div>
          <div class="info-value">${teacherData.email}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Phone</div>
          <div class="info-value">${teacherData.phone}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Subject</div>
          <div class="info-value">${teacherData.subject}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Qualification</div>
          <div class="info-value">${teacherData.qualification}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Experience</div>
          <div class="info-value">${teacherData.experience}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Joining Date</div>
          <div class="info-value">${new Date(teacherData.joinDate).toLocaleDateString()}</div>
        </div>
      </div>
    </div>
  `;
}

function initEditProfileForm() {
  const editFormDiv = document.getElementById('edit-profile-form');
  if (!editFormDiv) return;
  
  editFormDiv.innerHTML = `
    <div class="card" style="display: none;" id="profile-edit-card">
      <div class="card-header">
        <h2 class="card-title">Edit Profile</h2>
      </div>
      <form onsubmit="handleProfileSubmit(event)">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input type="text" class="form-input" value="${teacherData.name}" required>
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input type="email" class="form-input" value="${teacherData.email}" required>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Phone</label>
            <input type="tel" class="form-input" value="${teacherData.phone}" required>
          </div>
          <div class="form-group">
            <label class="form-label">Subject</label>
            <input type="text" class="form-input" value="${teacherData.subject}" required>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Qualification</label>
          <input type="text" class="form-input" value="${teacherData.qualification}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Profile Picture (Optional)</label>
          <input type="file" class="form-input" accept="image/*">
        </div>
        <div style="display: flex; gap: 1rem;">
          <button type="submit" class="btn btn-primary">Save Changes</button>
          <button type="button" class="btn btn-outline" onclick="toggleEditProfile()">Cancel</button>
        </div>
      </form>
    </div>
  `;
}

function toggleEditProfile() {
  const editCard = document.getElementById('profile-edit-card');
  if (editCard) {
    editCard.style.display = editCard.style.display === 'none' ? 'block' : 'none';
  }
}

function handleProfileSubmit(e) {
  e.preventDefault();
  alert('Profile updated successfully!');
  toggleEditProfile();
}

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  // Set active sidebar link
  setActiveSidebarLink();
  
  // Initialize mobile sidebar
  initMobileSidebar();
  
  // Initialize logout
  initLogout();
  
  // Page-specific initialization
  const currentPage = window.location.pathname.split('/').pop();
  
  switch(currentPage) {
    case 'teacher_dashboard.html':
      loadDashboard();
      break;
    case 'routine.html':
      loadRoutine();
      break;
    case 'course.html':
      loadCourseMaterials();
      initUploadForm();
      break;
    case 'assignments.html':
      loadAssignments();
      initAssignmentUploadForm();
      break;
    case 'results.html':
      loadResults();
      break;
    case 'attendance.html':
      loadAttendance();
      initAttendanceForm();
      break;
    case 'noticeboard.html':
      loadNotices();
      initNoticeForm();
      break;
    case 'profile.html':
      loadProfile();
      initEditProfileForm();
      break;
  }
  
  // Add fade-in animation
  document.querySelector('.main-content').classList.add('fade-in');
});
