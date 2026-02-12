// College Admin Portal - JavaScript Functionality

// Initialize Local Storage Data
function initializeData() {
  if (!localStorage.getItem('students')) {
    localStorage.setItem('students', JSON.stringify([
      { id: 1, name: 'John Doe', email: 'john@example.com', course: 'Computer Science', batch: '2024', semester: '1', phone: '123-456-7890', status: 'Active' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com', course: 'Mathematics', batch: '2024', semester: '1', phone: '123-456-7891', status: 'Active' },
      { id: 3, name: 'Mike Johnson', email: 'mike@example.com', course: 'Physics', batch: '2023', semester: '3', phone: '123-456-7892', status: 'Active' }
    ]));
  }

  if (!localStorage.getItem('teachers')) {
    localStorage.setItem('teachers', JSON.stringify([
      { id: 1, name: 'Dr. Sarah Williams', email: 'sarah@college.edu', subject: 'Computer Science', phone: '555-0001', status: 'Active' },
      { id: 2, name: 'Prof. Robert Brown', email: 'robert@college.edu', subject: 'Mathematics', phone: '555-0002', status: 'Active' }
    ]));
  }

  if (!localStorage.getItem('courses')) {
    localStorage.setItem('courses', JSON.stringify([
      { id: 1, name: 'Computer Science', code: 'CS101', teacher: 'Dr. Sarah Williams', credits: 4, semester: '1' },
      { id: 2, name: 'Mathematics', code: 'MATH101', teacher: 'Prof. Robert Brown', credits: 3, semester: '1' },
      { id: 3, name: 'Physics', code: 'PHY101', teacher: '', credits: 4, semester: '1' }
    ]));
  }

  if (!localStorage.getItem('assignments')) {
    localStorage.setItem('assignments', JSON.stringify([
      { id: 1, title: 'Data Structures Assignment', course: 'Computer Science', dueDate: '2026-03-01', description: 'Implement a binary tree', status: 'Active' },
      { id: 2, title: 'Calculus Problem Set', course: 'Mathematics', dueDate: '2026-02-25', description: 'Complete problems 1-20', status: 'Active' }
    ]));
  }

  if (!localStorage.getItem('results')) {
    localStorage.setItem('results', JSON.stringify([
      { id: 1, studentId: 1, studentName: 'John Doe', course: 'Computer Science', grade: 'A', marks: 92, maxMarks: 100 },
      { id: 2, studentId: 2, studentName: 'Jane Smith', course: 'Mathematics', grade: 'A+', marks: 97, maxMarks: 100 }
    ]));
  }

  if (!localStorage.getItem('attendance')) {
    localStorage.setItem('attendance', JSON.stringify([
      { id: 1, studentId: 1, studentName: 'John Doe', course: 'Computer Science', date: '2026-02-12', status: 'Present' },
      { id: 2, studentId: 2, studentName: 'Jane Smith', course: 'Mathematics', date: '2026-02-12', status: 'Present' }
    ]));
  }

  if (!localStorage.getItem('notices')) {
    localStorage.setItem('notices', JSON.stringify([
      { id: 1, title: 'Mid-term Exam Schedule', content: 'Mid-term exams will be held from March 1-15, 2026.', date: '2026-02-10', target: 'All Students', priority: 'High' },
      { id: 2, title: 'Library Hours Extended', content: 'Library will be open until 10 PM during exam period.', date: '2026-02-11', target: 'All Students', priority: 'Medium' }
    ]));
  }

  if (!localStorage.getItem('fees')) {
    localStorage.setItem('fees', JSON.stringify([
      { id: 1, studentId: 1, studentName: 'John Doe', course: 'Computer Science', totalFees: 50000, paidAmount: 30000, remainingBalance: 20000, status: 'Partial', semester: '1', batch: '2024' },
      { id: 2, studentId: 2, studentName: 'Jane Smith', course: 'Mathematics', totalFees: 45000, paidAmount: 45000, remainingBalance: 0, status: 'Paid', semester: '1', batch: '2024' },
      { id: 3, studentId: 3, studentName: 'Mike Johnson', course: 'Physics', totalFees: 48000, paidAmount: 0, remainingBalance: 48000, status: 'Unpaid', semester: '3', batch: '2023' }
    ]));
  }

  if (!localStorage.getItem('adminProfile')) {
    localStorage.setItem('adminProfile', JSON.stringify({
      name: 'Admin User',
      email: 'admin@college.edu',
      phone: '555-1234',
      role: 'System Administrator',
      joinDate: '2020-01-15'
    }));
  }
}

// Utility Functions
function getFromStorage(key) {
  return JSON.parse(localStorage.getItem(key)) || [];
}

function saveToStorage(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}

function generateId(items) {
  return items.length > 0 ? Math.max(...items.map(item => item.id)) + 1 : 1;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Highlight Active Navigation
function highlightActiveNav() {
  const currentPage = window.location.pathname.split('/').pop();
  const navLinks = document.querySelectorAll('.nav-item a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });
}

// Show Alert Message
function showAlert(message, type = 'success') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} fade-in`;
  alertDiv.innerHTML = `
    <span>✓</span>
    <span>${message}</span>
  `;
  
  document.querySelector('.main-content').insertBefore(
    alertDiv,
    document.querySelector('.main-content').firstChild
  );
  
  setTimeout(() => {
    alertDiv.style.opacity = '0';
    setTimeout(() => alertDiv.remove(), 300);
  }, 3000);
}

// Modal Functions
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
  }
}

// Dashboard Functions
function loadDashboardStats() {
  const students = getFromStorage('students');
  const teachers = getFromStorage('teachers');
  const courses = getFromStorage('courses');
  const assignments = getFromStorage('assignments');
  const notices = getFromStorage('notices');

  document.getElementById('total-students').textContent = students.length;
  document.getElementById('total-teachers').textContent = teachers.length;
  document.getElementById('total-courses').textContent = courses.length;
  document.getElementById('total-assignments').textContent = assignments.length;
  document.getElementById('total-notices').textContent = notices.length;
}

function loadRecentActivity() {
  const activityList = document.getElementById('recent-activity');
  if (!activityList) return;

  const students = getFromStorage('students');
  const notices = getFromStorage('notices');
  const assignments = getFromStorage('assignments');

  let activities = [];

  // Recent students
  students.slice(-3).reverse().forEach(student => {
    activities.push({
      title: `New student enrolled: ${student.name}`,
      time: 'Recently added',
      type: 'student'
    });
  });

  // Recent notices
  notices.slice(-2).reverse().forEach(notice => {
    activities.push({
      title: `Notice posted: ${notice.title}`,
      time: formatDate(notice.date),
      type: 'notice'
    });
  });

  activityList.innerHTML = activities.map(activity => `
    <li class="activity-item slide-in">
      <div class="activity-title">${activity.title}</div>
      <div class="activity-time">${activity.time}</div>
    </li>
  `).join('');
}

// Student Management Functions
function loadStudents() {
  const students = getFromStorage('students');
  const tbody = document.querySelector('#student-table tbody');
  if (!tbody) return;

  tbody.innerHTML = students.map(student => `
    <tr>
      <td>${student.id}</td>
      <td>${student.name}</td>
      <td>${student.email}</td>
      <td>${student.course}</td>
      <td>${student.batch}</td>
      <td>${student.semester}</td>
      <td><span class="badge badge-${student.status === 'Active' ? 'success' : 'danger'}">${student.status}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="editStudent(${student.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteStudent(${student.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function addStudent(event) {
  event.preventDefault();
  const form = event.target;
  const students = getFromStorage('students');

  const newStudent = {
    id: generateId(students),
    name: form.studentName.value,
    email: form.studentEmail.value,
    course: form.studentCourse.value,
    batch: form.studentBatch.value,
    semester: form.studentSemester.value,
    phone: form.studentPhone.value,
    status: form.studentStatus.value
  };

  students.push(newStudent);
  saveToStorage('students', students);
  loadStudents();
  form.reset();
  closeModal('studentModal');
  showAlert('Student added successfully!');
}

function editStudent(id) {
  const students = getFromStorage('students');
  const student = students.find(s => s.id === id);
  
  if (student) {
    document.getElementById('studentName').value = student.name;
    document.getElementById('studentEmail').value = student.email;
    document.getElementById('studentCourse').value = student.course;
    document.getElementById('studentBatch').value = student.batch;
    document.getElementById('studentSemester').value = student.semester;
    document.getElementById('studentPhone').value = student.phone;
    document.getElementById('studentStatus').value = student.status;
    
    openModal('studentModal');
    
    // Update form to edit mode
    const form = document.getElementById('student-form');
    form.setAttribute('data-edit-id', id);
  }
}

function deleteStudent(id) {
  if (confirm('Are you sure you want to delete this student?')) {
    let students = getFromStorage('students');
    students = students.filter(s => s.id !== id);
    saveToStorage('students', students);
    loadStudents();
    showAlert('Student deleted successfully!', 'danger');
  }
}

// Teacher Management Functions
function loadTeachers() {
  const teachers = getFromStorage('teachers');
  const tbody = document.querySelector('#teacher-table tbody');
  if (!tbody) return;

  tbody.innerHTML = teachers.map(teacher => `
    <tr>
      <td>${teacher.id}</td>
      <td>${teacher.name}</td>
      <td>${teacher.email}</td>
      <td>${teacher.subject}</td>
      <td>${teacher.phone}</td>
      <td><span class="badge badge-${teacher.status === 'Active' ? 'success' : 'danger'}">${teacher.status}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="editTeacher(${teacher.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteTeacher(${teacher.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function addTeacher(event) {
  event.preventDefault();
  const form = event.target;
  const teachers = getFromStorage('teachers');

  const newTeacher = {
    id: generateId(teachers),
    name: form.teacherName.value,
    email: form.teacherEmail.value,
    subject: form.teacherSubject.value,
    phone: form.teacherPhone.value,
    status: form.teacherStatus.value
  };

  teachers.push(newTeacher);
  saveToStorage('teachers', teachers);
  loadTeachers();
  form.reset();
  closeModal('teacherModal');
  showAlert('Teacher added successfully!');
}

function editTeacher(id) {
  const teachers = getFromStorage('teachers');
  const teacher = teachers.find(t => t.id === id);
  
  if (teacher) {
    document.getElementById('teacherName').value = teacher.name;
    document.getElementById('teacherEmail').value = teacher.email;
    document.getElementById('teacherSubject').value = teacher.subject;
    document.getElementById('teacherPhone').value = teacher.phone;
    document.getElementById('teacherStatus').value = teacher.status;
    
    openModal('teacherModal');
  }
}

function deleteTeacher(id) {
  if (confirm('Are you sure you want to delete this teacher?')) {
    let teachers = getFromStorage('teachers');
    teachers = teachers.filter(t => t.id !== id);
    saveToStorage('teachers', teachers);
    loadTeachers();
    showAlert('Teacher deleted successfully!', 'danger');
  }
}

// Course Management Functions
function loadCourses() {
  const courses = getFromStorage('courses');
  const tbody = document.querySelector('#courses-table tbody');
  if (!tbody) return;

  tbody.innerHTML = courses.map(course => `
    <tr>
      <td>${course.id}</td>
      <td>${course.name}</td>
      <td>${course.code}</td>
      <td>${course.teacher || 'Not Assigned'}</td>
      <td>${course.credits}</td>
      <td>${course.semester}</td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="editCourse(${course.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteCourse(${course.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function loadTeacherOptions() {
  const teachers = getFromStorage('teachers');
  const select = document.getElementById('courseTeacher');
  if (!select) return;

  select.innerHTML = '<option value="">Select Teacher</option>' +
    teachers.map(teacher => `<option value="${teacher.name}">${teacher.name}</option>`).join('');
}

function addCourse(event) {
  event.preventDefault();
  const form = event.target;
  const courses = getFromStorage('courses');

  const newCourse = {
    id: generateId(courses),
    name: form.courseName.value,
    code: form.courseCode.value,
    teacher: form.courseTeacher.value,
    credits: form.courseCredits.value,
    semester: form.courseSemester.value
  };

  courses.push(newCourse);
  saveToStorage('courses', courses);
  loadCourses();
  form.reset();
  closeModal('courseModal');
  showAlert('Course added successfully!');
}

function editCourse(id) {
  const courses = getFromStorage('courses');
  const course = courses.find(c => c.id === id);
  
  if (course) {
    document.getElementById('courseName').value = course.name;
    document.getElementById('courseCode').value = course.code;
    document.getElementById('courseTeacher').value = course.teacher;
    document.getElementById('courseCredits').value = course.credits;
    document.getElementById('courseSemester').value = course.semester;
    
    openModal('courseModal');
  }
}

function deleteCourse(id) {
  if (confirm('Are you sure you want to delete this course?')) {
    let courses = getFromStorage('courses');
    courses = courses.filter(c => c.id !== id);
    saveToStorage('courses', courses);
    loadCourses();
    showAlert('Course deleted successfully!', 'danger');
  }
}

// Assignment Management Functions
function loadAssignments() {
  const assignments = getFromStorage('assignments');
  const tbody = document.querySelector('#assignments-table tbody');
  if (!tbody) return;

  tbody.innerHTML = assignments.map(assignment => `
    <tr>
      <td>${assignment.id}</td>
      <td>${assignment.title}</td>
      <td>${assignment.course}</td>
      <td>${formatDate(assignment.dueDate)}</td>
      <td><span class="badge badge-${assignment.status === 'Active' ? 'info' : 'success'}">${assignment.status}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="editAssignment(${assignment.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteAssignment(${assignment.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function loadCourseOptions() {
  const courses = getFromStorage('courses');
  const select = document.getElementById('assignmentCourse');
  if (!select) return;

  select.innerHTML = '<option value="">Select Course</option>' +
    courses.map(course => `<option value="${course.name}">${course.name}</option>`).join('');
}

function addAssignment(event) {
  event.preventDefault();
  const form = event.target;
  const assignments = getFromStorage('assignments');

  const newAssignment = {
    id: generateId(assignments),
    title: form.assignmentTitle.value,
    course: form.assignmentCourse.value,
    dueDate: form.assignmentDueDate.value,
    description: form.assignmentDescription.value,
    status: form.assignmentStatus.value
  };

  assignments.push(newAssignment);
  saveToStorage('assignments', assignments);
  loadAssignments();
  form.reset();
  closeModal('assignmentModal');
  showAlert('Assignment added successfully!');
}

function editAssignment(id) {
  const assignments = getFromStorage('assignments');
  const assignment = assignments.find(a => a.id === id);
  
  if (assignment) {
    document.getElementById('assignmentTitle').value = assignment.title;
    document.getElementById('assignmentCourse').value = assignment.course;
    document.getElementById('assignmentDueDate').value = assignment.dueDate;
    document.getElementById('assignmentDescription').value = assignment.description;
    document.getElementById('assignmentStatus').value = assignment.status;
    
    openModal('assignmentModal');
  }
}

function deleteAssignment(id) {
  if (confirm('Are you sure you want to delete this assignment?')) {
    let assignments = getFromStorage('assignments');
    assignments = assignments.filter(a => a.id !== id);
    saveToStorage('assignments', assignments);
    loadAssignments();
    showAlert('Assignment deleted successfully!', 'danger');
  }
}

// Results Management Functions
function loadResults() {
  const results = getFromStorage('results');
  const tbody = document.querySelector('#results-table tbody');
  if (!tbody) return;

  tbody.innerHTML = results.map(result => `
    <tr>
      <td>${result.id}</td>
      <td>${result.studentName}</td>
      <td>${result.course}</td>
      <td>${result.marks}/${result.maxMarks}</td>
      <td><span class="badge badge-success">${result.grade}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="editResult(${result.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteResult(${result.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function loadStudentOptions() {
  const students = getFromStorage('students');
  const select = document.getElementById('resultStudent');
  if (!select) return;

  select.innerHTML = '<option value="">Select Student</option>' +
    students.map(student => `<option value="${student.id}">${student.name}</option>`).join('');
}

function addResult(event) {
  event.preventDefault();
  const form = event.target;
  const results = getFromStorage('results');
  const students = getFromStorage('students');
  
  const studentId = parseInt(form.resultStudent.value);
  const student = students.find(s => s.id === studentId);

  const newResult = {
    id: generateId(results),
    studentId: studentId,
    studentName: student ? student.name : 'Unknown',
    course: form.resultCourse.value,
    marks: parseInt(form.resultMarks.value),
    maxMarks: parseInt(form.resultMaxMarks.value),
    grade: form.resultGrade.value
  };

  results.push(newResult);
  saveToStorage('results', results);
  loadResults();
  form.reset();
  closeModal('resultModal');
  showAlert('Result added successfully!');
}

function editResult(id) {
  const results = getFromStorage('results');
  const result = results.find(r => r.id === id);
  
  if (result) {
    document.getElementById('resultStudent').value = result.studentId;
    document.getElementById('resultCourse').value = result.course;
    document.getElementById('resultMarks').value = result.marks;
    document.getElementById('resultMaxMarks').value = result.maxMarks;
    document.getElementById('resultGrade').value = result.grade;
    
    openModal('resultModal');
  }
}

function deleteResult(id) {
  if (confirm('Are you sure you want to delete this result?')) {
    let results = getFromStorage('results');
    results = results.filter(r => r.id !== id);
    saveToStorage('results', results);
    loadResults();
    showAlert('Result deleted successfully!', 'danger');
  }
}

// Attendance Management Functions
function loadAttendance() {
  const attendance = getFromStorage('attendance');
  const tbody = document.querySelector('#attendance-table tbody');
  if (!tbody) return;

  tbody.innerHTML = attendance.map(record => `
    <tr>
      <td>${record.id}</td>
      <td>${record.studentName}</td>
      <td>${record.course}</td>
      <td>${formatDate(record.date)}</td>
      <td><span class="badge badge-${record.status === 'Present' ? 'success' : 'danger'}">${record.status}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="editAttendance(${record.id})">Edit</button>
        <button class="btn btn-sm btn-danger" onclick="deleteAttendance(${record.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function addAttendance(event) {
  event.preventDefault();
  const form = event.target;
  const attendance = getFromStorage('attendance');
  const students = getFromStorage('students');
  
  const studentId = parseInt(form.attendanceStudent.value);
  const student = students.find(s => s.id === studentId);

  const newAttendance = {
    id: generateId(attendance),
    studentId: studentId,
    studentName: student ? student.name : 'Unknown',
    course: form.attendanceCourse.value,
    date: form.attendanceDate.value,
    status: form.attendanceStatus.value
  };

  attendance.push(newAttendance);
  saveToStorage('attendance', attendance);
  loadAttendance();
  form.reset();
  closeModal('attendanceModal');
  showAlert('Attendance marked successfully!');
}

function editAttendance(id) {
  const attendance = getFromStorage('attendance');
  const record = attendance.find(a => a.id === id);
  
  if (record) {
    document.getElementById('attendanceStudent').value = record.studentId;
    document.getElementById('attendanceCourse').value = record.course;
    document.getElementById('attendanceDate').value = record.date;
    document.getElementById('attendanceStatus').value = record.status;
    
    openModal('attendanceModal');
  }
}

function deleteAttendance(id) {
  if (confirm('Are you sure you want to delete this attendance record?')) {
    let attendance = getFromStorage('attendance');
    attendance = attendance.filter(a => a.id !== id);
    saveToStorage('attendance', attendance);
    loadAttendance();
    showAlert('Attendance record deleted successfully!', 'danger');
  }
}

// Notice Management Functions
function loadNotices() {
  const notices = getFromStorage('notices');
  const noticeList = document.getElementById('notice-list');
  if (!noticeList) return;

  noticeList.innerHTML = notices.map(notice => `
    <div class="card slide-in">
      <div class="card-header">
        <div>
          <h3 class="card-title">${notice.title}</h3>
          <p class="text-muted mb-0">${formatDate(notice.date)} • ${notice.target} • <span class="badge badge-${notice.priority === 'High' ? 'danger' : notice.priority === 'Medium' ? 'warning' : 'info'}">${notice.priority}</span></p>
        </div>
        <div class="table-actions">
          <button class="btn btn-sm btn-primary" onclick="editNotice(${notice.id})">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="deleteNotice(${notice.id})">Delete</button>
        </div>
      </div>
      <div class="card-body">
        <p>${notice.content}</p>
      </div>
    </div>
  `).join('');
}

function addNotice(event) {
  event.preventDefault();
  const form = event.target;
  const notices = getFromStorage('notices');

  const newNotice = {
    id: generateId(notices),
    title: form.noticeTitle.value,
    content: form.noticeContent.value,
    date: form.noticeDate.value,
    target: form.noticeTarget.value,
    priority: form.noticePriority.value
  };

  notices.push(newNotice);
  saveToStorage('notices', notices);
  loadNotices();
  form.reset();
  closeModal('noticeModal');
  showAlert('Notice posted successfully!');
}

function editNotice(id) {
  const notices = getFromStorage('notices');
  const notice = notices.find(n => n.id === id);
  
  if (notice) {
    document.getElementById('noticeTitle').value = notice.title;
    document.getElementById('noticeContent').value = notice.content;
    document.getElementById('noticeDate').value = notice.date;
    document.getElementById('noticeTarget').value = notice.target;
    document.getElementById('noticePriority').value = notice.priority;
    
    openModal('noticeModal');
  }
}

function deleteNotice(id) {
  if (confirm('Are you sure you want to delete this notice?')) {
    let notices = getFromStorage('notices');
    notices = notices.filter(n => n.id !== id);
    saveToStorage('notices', notices);
    loadNotices();
    showAlert('Notice deleted successfully!', 'danger');
  }
}

// Fee Management Functions
function loadFees() {
  const fees = getFromStorage('fees');
  const tbody = document.querySelector('#fee-status tbody');
  if (!tbody) return;

  tbody.innerHTML = fees.map(fee => `
    <tr>
      <td>${fee.id}</td>
      <td>${fee.studentName}</td>
      <td>${fee.course}</td>
      <td>${fee.semester}</td>
      <td>₹${fee.totalFees.toLocaleString()}</td>
      <td>₹${fee.paidAmount.toLocaleString()}</td>
      <td>₹${fee.remainingBalance.toLocaleString()}</td>
      <td><span class="badge badge-${fee.status === 'Paid' ? 'success' : fee.status === 'Partial' ? 'warning' : 'danger'}">${fee.status}</span></td>
      <td class="table-actions">
        <button class="btn btn-sm btn-primary" onclick="updateFee(${fee.id})">Update</button>
      </td>
    </tr>
  `).join('');
}

function updateFee(id) {
  const fees = getFromStorage('fees');
  const fee = fees.find(f => f.id === id);
  
  if (fee) {
    document.getElementById('feeStudentName').value = fee.studentName;
    document.getElementById('feeTotalAmount').value = fee.totalFees;
    document.getElementById('feePaidAmount').value = fee.paidAmount;
    document.getElementById('feeStatus').value = fee.status;
    
    openModal('feeModal');
    
    const form = document.getElementById('fee-update-form');
    form.setAttribute('data-fee-id', id);
  }
}

function saveFeeUpdate(event) {
  event.preventDefault();
  const form = event.target;
  const feeId = parseInt(form.getAttribute('data-fee-id'));
  const fees = getFromStorage('fees');
  
  const feeIndex = fees.findIndex(f => f.id === feeId);
  if (feeIndex !== -1) {
    const paidAmount = parseInt(form.feePaidAmount.value);
    const totalFees = parseInt(form.feeTotalAmount.value);
    
    fees[feeIndex].paidAmount = paidAmount;
    fees[feeIndex].totalFees = totalFees;
    fees[feeIndex].remainingBalance = totalFees - paidAmount;
    fees[feeIndex].status = form.feeStatus.value;
    
    saveToStorage('fees', fees);
    loadFees();
    closeModal('feeModal');
    showAlert('Fee updated successfully!');
  }
}

// Profile Management Functions
function loadProfile() {
  const profile = JSON.parse(localStorage.getItem('adminProfile'));
  if (!profile) return;

  document.getElementById('profileName').textContent = profile.name;
  document.getElementById('profileEmail').textContent = profile.email;
  document.getElementById('profilePhone').textContent = profile.phone;
  document.getElementById('profileRole').textContent = profile.role;
  document.getElementById('profileJoinDate').textContent = formatDate(profile.joinDate);

  // Populate edit form
  document.getElementById('editName').value = profile.name;
  document.getElementById('editEmail').value = profile.email;
  document.getElementById('editPhone').value = profile.phone;
}

function saveProfile(event) {
  event.preventDefault();
  const form = event.target;

  const profile = {
    name: form.editName.value,
    email: form.editEmail.value,
    phone: form.editPhone.value,
    role: 'System Administrator',
    joinDate: JSON.parse(localStorage.getItem('adminProfile')).joinDate
  };

  localStorage.setItem('adminProfile', JSON.stringify(profile));
  loadProfile();
  closeModal('editProfileModal');
  showAlert('Profile updated successfully!');
}

// Logout Function
function logout() {
  if (confirm('Are you sure you want to logout?')) {
    // Could clear session data here if needed
    window.location.href = 'login.html';
  }
}

// Search and Filter Functions
function searchTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  const filter = input.value.toUpperCase();
  const table = document.getElementById(tableId);
  const tr = table.getElementsByTagName('tr');

  for (let i = 1; i < tr.length; i++) {
    let found = false;
    const td = tr[i].getElementsByTagName('td');
    
    for (let j = 0; j < td.length; j++) {
      if (td[j]) {
        const txtValue = td[j].textContent || td[j].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          found = true;
          break;
        }
      }
    }
    
    tr[i].style.display = found ? '' : 'none';
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  initializeData();
  highlightActiveNav();

  // Close modal when clicking outside
  window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
      event.target.classList.remove('active');
    }
  };
});
