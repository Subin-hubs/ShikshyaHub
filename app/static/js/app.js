/**
 * ShikshyaHub - Global JavaScript Handler
 * Handles all form submissions, AJAX requests, and button interactions
 */

// ==================== CONFIGURATION ====================
const API_BASE = window.location.origin;
const ROLES = {
    ADMIN: 'admin',
    TEACHER: 'teacher',
    STUDENT: 'student'
};

// ==================== UTILITY FUNCTIONS ====================

/**
 * Make API request
 */
async function apiRequest(method, endpoint, data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'Request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const container = document.querySelector('.content-wrapper') || document.body;
    const alertDiv = document.createElement('div');
    alertDiv.innerHTML = alertHTML;
    container.insertBefore(alertDiv.firstChild, container.firstChild);

    // Auto dismiss
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Format date
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// ==================== FORM HANDLERS ====================

/**
 * Handle Add User Form (Admin)
 */
document.addEventListener('submit', async function (e) {
    if (e.target.id === 'addUserForm') {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            password: formData.get('password'),
            role: formData.get('role'),
            student_id_no: formData.get('student_id_no'),
            year: formData.get('year'),
            semester: formData.get('semester'),
            employee_id: formData.get('employee_id'),
            department: formData.get('department')
        };

        try {
            const result = await apiRequest('POST', '/admin/api/add-user', data);
            showNotification('User added successfully!', 'success');
            e.target.reset();

            // Close modal and refresh
            const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
            if (modal) modal.hide();
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error adding user:', error);
        }
    }
});

/**
 * Handle Add Course Form (Teacher/Admin)
 */
document.addEventListener('submit', async function (e) {
    if (e.target.id === 'addCourseForm') {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            code: formData.get('code')
        };

        const endpoint = window.location.pathname.includes('/admin/')
            ? '/admin/api/add-course'
            : '/teacher/api/add-course';

        try {
            const result = await apiRequest('POST', endpoint, data);
            showNotification('Course added successfully!', 'success');
            e.target.reset();

            const modal = bootstrap.Modal.getInstance(document.getElementById('addCourseModal'));
            if (modal) modal.hide();
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error adding course:', error);
        }
    }
});

/**
 * Handle Mark Attendance Form (Teacher)
 */
document.addEventListener('submit', async function (e) {
    if (e.target.id === 'markAttendanceForm') {
        e.preventDefault();

        const courseId = document.getElementById('attendanceCourseSelect').value;
        const attendance = {};

        // Collect attendance data
        document.querySelectorAll('.attendance-checkbox').forEach(checkbox => {
            const studentId = checkbox.dataset.studentId;
            attendance[studentId] = checkbox.checked ? 'Present' : 'Absent';
        });

        try {
            const result = await apiRequest('POST', '/teacher/api/mark-attendance', {
                course_id: courseId,
                attendance: attendance
            });
            showNotification('Attendance marked successfully!', 'success');

            const modal = bootstrap.Modal.getInstance(document.getElementById('markAttendanceModal'));
            if (modal) modal.hide();
        } catch (error) {
            console.error('Error marking attendance:', error);
        }
    }
});

/**
 * Handle Add Assignment Form (Teacher)
 */
document.addEventListener('submit', async function (e) {
    if (e.target.id === 'addAssignmentForm') {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = {
            course_id: formData.get('course_id'),
            title: formData.get('title'),
            due_date: formData.get('due_date')
        };

        try {
            const result = await apiRequest('POST', '/teacher/api/add-assignment', data);
            showNotification('Assignment added successfully!', 'success');
            e.target.reset();

            const modal = bootstrap.Modal.getInstance(document.getElementById('addAssignmentModal'));
            if (modal) modal.hide();
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error adding assignment:', error);
        }
    }
});

/**
 * Handle Add Grade Form (Teacher)
 */
document.addEventListener('submit', async function (e) {
    if (e.target.id === 'addGradeForm') {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = {
            student_id: formData.get('student_id'),
            course_id: formData.get('course_id'),
            marks: parseFloat(formData.get('marks')),
            total: parseFloat(formData.get('total'))
        };

        try {
            const result = await apiRequest('POST', '/teacher/api/add-grade', data);
            showNotification('Grade added successfully!', 'success');
            e.target.reset();

            const modal = bootstrap.Modal.getInstance(document.getElementById('addGradeModal'));
            if (modal) modal.hide();
        } catch (error) {
            console.error('Error adding grade:', error);
        }
    }
});

// ==================== BUTTON CLICK HANDLERS ====================

/**
 * Handle Delete User Button
 */
document.addEventListener('click', async function (e) {
    if (e.target.classList.contains('btn-delete-user')) {
        if (!confirm('Are you sure you want to delete this user?')) return;

        const userId = e.target.dataset.userId;
        try {
            const result = await apiRequest('DELETE', `/admin/api/delete-user/${userId}`);
            showNotification('User deleted successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    }
});

/**
 * Handle Edit User Button
 */
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-edit-user')) {
        const userId = e.target.dataset.userId;
        const userName = e.target.dataset.userName;
        const userEmail = e.target.dataset.userEmail;
        const userRole = e.target.dataset.userRole;

        // Pre-fill form
        document.getElementById('editUserId').value = userId;
        document.getElementById('editUserName').value = userName;
        document.getElementById('editUserEmail').value = userEmail;
        document.getElementById('editUserRole').value = userRole;

        const modal = new bootstrap.Modal(document.getElementById('editUserModal'));
        modal.show();
    }
});

/**
 * Handle Delete Course Button
 */
document.addEventListener('click', async function (e) {
    if (e.target.classList.contains('btn-delete-course')) {
        if (!confirm('Are you sure you want to delete this course?')) return;

        const courseId = e.target.dataset.courseId;
        const endpoint = window.location.pathname.includes('/admin/')
            ? `/admin/api/delete-course/${courseId}`
            : `/teacher/api/delete-course/${courseId}`;

        try {
            const result = await apiRequest('DELETE', endpoint);
            showNotification('Course deleted successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error deleting course:', error);
        }
    }
});

/**
 * Handle Edit Course Button
 */
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-edit-course')) {
        const courseId = e.target.dataset.courseId;
        const courseName = e.target.dataset.courseName;
        const courseCode = e.target.dataset.courseCode;

        document.getElementById('editCourseId').value = courseId;
        document.getElementById('editCourseName').value = courseName;
        document.getElementById('editCourseCode').value = courseCode;

        const modal = new bootstrap.Modal(document.getElementById('editCourseModal'));
        modal.show();
    }
});

/**
 * Handle Enroll Course Button (Student)
 */
document.addEventListener('click', async function (e) {
    if (e.target.classList.contains('btn-enroll-course')) {
        const courseId = e.target.dataset.courseId;
        try {
            const result = await apiRequest('POST', `/student/api/enroll/${courseId}`);
            showNotification('Enrolled in course successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error enrolling course:', error);
        }
    }
});

/**
 * Handle Unenroll Course Button (Student)
 */
document.addEventListener('click', async function (e) {
    if (e.target.classList.contains('btn-unenroll-course')) {
        if (!confirm('Are you sure you want to unenroll from this course?')) return;

        const courseId = e.target.dataset.courseId;
        try {
            const result = await apiRequest('POST', `/student/api/unenroll/${courseId}`);
            showNotification('Unenrolled from course successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error unenrolling from course:', error);
        }
    }
});

/**
 * Handle Submit Assignment Button (Student)
 */
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-submit-assignment')) {
        const assignmentId = e.target.dataset.assignmentId;
        document.getElementById('submitAssignmentId').value = assignmentId;
    }
});

/**
 * Handle Submit Assignment Form
 */
document.addEventListener('submit', async function (e) {
    if (e.target.id === 'submitAssignmentForm') {
        e.preventDefault();

        const assignmentId = document.getElementById('submitAssignmentId').value;
        const fileInput = document.getElementById('assignmentFile');
        const file = fileInput.files[0];

        if (!file) {
            showNotification('Please select a file', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE}/student/api/submit-assignment/${assignmentId}`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || 'Submission failed');
            }

            showNotification('Assignment submitted successfully!', 'success');
            e.target.reset();

            const modal = bootstrap.Modal.getInstance(document.getElementById('submitModal'));
            if (modal) modal.hide();
        } catch (error) {
            console.error('Error submitting assignment:', error);
            showNotification(error.message, 'error');
        }
    }
});

/**
 * Handle Bulk Enroll Button (Admin)
 */
document.addEventListener('click', async function (e) {
    if (e.target.classList.contains('btn-bulk-enroll')) {
        const courseId = e.target.dataset.courseId;

        // Get selected students
        const studentIds = Array.from(document.querySelectorAll('.student-checkbox:checked'))
            .map(cb => cb.dataset.studentId);

        if (studentIds.length === 0) {
            showNotification('Please select at least one student', 'warning');
            return;
        }

        try {
            const result = await apiRequest('POST', '/admin/api/bulk-enroll', {
                course_id: courseId,
                student_ids: studentIds
            });
            showNotification(`${studentIds.length} students enrolled successfully!`, 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Error bulk enrolling:', error);
        }
    }
});

/**
 * Handle System Backup Button (Admin)
 */
document.addEventListener('click', async function (e) {
    if (e.target.classList.contains('btn-system-backup')) {
        if (!confirm('This will create a system backup. Continue?')) return;

        try {
            const result = await apiRequest('POST', '/admin/api/system-backup');
            showNotification('System backup created successfully!', 'success');
        } catch (error) {
            console.error('Error creating backup:', error);
        }
    }
});

// ==================== SEARCH & FILTER ====================

/**
 * Search functionality for user table
 */
document.addEventListener('keyup', function (e) {
    if (e.target.id === 'userSearchInput') {
        const searchValue = e.target.value.toLowerCase();
        document.querySelectorAll('tbody tr').forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchValue) ? '' : 'none';
        });
    }
});

/**
 * Search functionality for course grid
 */
document.addEventListener('keyup', function (e) {
    if (e.target.id === 'searchInput') {
        const searchValue = e.target.value.toLowerCase();
        document.querySelectorAll('.course-card').forEach(card => {
            const courseData = card.getAttribute('data-course').toLowerCase();
            card.style.display = courseData.includes(searchValue) ? '' : 'none';
        });
    }
});

// ==================== INITIALIZATION ====================

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// ==================== EXPORT ====================

window.ShikshyaHub = {
    apiRequest,
    showNotification,
    formatDate,
    API_BASE,
    ROLES
};
