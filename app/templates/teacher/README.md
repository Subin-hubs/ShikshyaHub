# Teacher Portal - Sidebar Layout

A complete, professional teacher portal with sidebar navigation and blue color theme.

## 📂 Folder Structure

```
teacher-portal/
├── css/
│   └── style.css          # All styling with blue theme
├── js/
│   └── script.js          # All JavaScript functionality
├── teacher_dashboard.html
├── routine.html
├── course.html
├── assignments.html
├── results.html
├── attendance.html
├── noticeboard.html
└── profile.html
```

## 🎨 Design Features

### Color Theme
- **Primary Color**: Blue (#1E90FF)
- **Sidebar Background**: Blue (#1E90FF)
- **Sidebar Active**: Darker Blue (#1873CC)
- **Background**: White & Light Gray (#F5F7FA)
- **Text**: Dark Blue/Black for readability

### Layout
- **Sidebar Navigation** on the left (260px width)
- **Main Content Area** on the right
- **Responsive design** - sidebar collapses on mobile
- **Professional shadows** on cards and tables
- **Clean, modern typography** using Poppins font

## 📄 Pages & Features

### 1. **Dashboard** (teacher_dashboard.html)
- Welcome message with teacher info
- 4 Stats cards:
  - Total Students (8)
  - Assignments Uploaded (4)
  - Attendance Overview (89.9%)
  - Notices Posted (4)
- Recent activity feed
- **IDs**: `teacher-info`, `teacher-stats`, `recent-activity`

### 2. **Routine** (routine.html)
- Weekly class schedule table
- Shows time slots, subjects, rooms, and class types
- Monday through Friday schedule
- **IDs**: `routine-table`

### 3. **Course** (course.html)
- Upload course materials form
- View all uploaded materials (PDF, PPTX, MP4, etc.)
- Download tracking
- Delete functionality
- **IDs**: `course-materials`, `upload-form`

### 4. **Assignments** (assignments.html)
- Upload new assignments
- View all assignments with submission tracking
- Due dates and status badges
- View submissions and delete options
- **IDs**: `assignments-table`, `upload-assignment-form`

### 5. **Results** (results.html)
- Student results table with grades
- Shows Midterm, Final, Assignments, Total scores
- Grade badges (A+, A, B+, B, C+)
- Results summary with class statistics
- Edit grade functionality
- **IDs**: `results-table`, `results-summary`

### 6. **Attendance** (attendance.html)
- Mark today's attendance form
- View attendance records for all students
- Attendance percentage tracking
- Color-coded status badges
- **IDs**: `attendance-table`, `attendance-form`

### 7. **Noticeboard** (noticeboard.html)
- Post new notices
- View all posted notices
- Urgent notice highlighting (red border)
- Edit and delete functionality
- Sorted by date (newest first)
- **IDs**: `notice-list`, `notice-form`

### 8. **Profile** (profile.html)
- View teacher information
- Edit profile form (toggle)
- Upload profile picture option
- Shows: ID, Email, Phone, Subject, Qualification, Experience
- **IDs**: `profile-info`, `edit-profile-form`

### 9. **Logout**
- Available on all pages in sidebar
- Clears localStorage and sessionStorage
- Confirmation dialog
- **ID**: `logout-btn`

## 📊 Dummy Data Included

### Teacher Data
- Name: Prof. Michael Anderson
- Subject: Computer Science
- 8 years experience
- Ph.D. in Computer Science

### Students Data (8 Students)
- Complete with names, emails, grades, scores, attendance
- Examples: Emma Wilson (A), Sophia Martinez (A+), Lucas Lee (C+)

### Course Materials (4 Items)
- Lecture notes, presentations, videos, practice problems
- File types: PDF, PPTX, MP4
- Download tracking included

### Assignments (4 Items)
- Binary Search Tree Implementation
- Sorting Algorithm Analysis
- Graph Traversal Project
- Database Design Assignment

### Routine Data
- Monday to Friday schedule
- Multiple time slots per day
- Includes lectures, labs, office hours, meetings

### Notices (4 Items)
- Mid-semester exam schedule
- Assignment deadline extension
- Guest lecture announcement
- Lab session rescheduled

## 🎯 All Required IDs Present

✅ `teacher-info` - Dashboard teacher welcome  
✅ `teacher-stats` - Dashboard stats cards  
✅ `recent-activity` - Recent activity feed  
✅ `routine-table` - Weekly schedule table  
✅ `course-materials` - Uploaded materials list  
✅ `upload-form` - Material upload form  
✅ `assignments-table` - All assignments table  
✅ `upload-assignment-form` - Assignment upload form  
✅ `results-table` - Student results table  
✅ `results-summary` - Results statistics  
✅ `attendance-table` - Attendance records  
✅ `attendance-form` - Mark attendance form  
✅ `notice-list` - All notices list  
✅ `notice-form` - Post notice form  
✅ `profile-info` - Profile information  
✅ `edit-profile-form` - Edit profile form  
✅ `logout-btn` - Logout button  

## 🚀 How to Use

1. **Open any HTML file** in a web browser
2. **Navigate** using the sidebar menu
3. **Active page** is highlighted with darker blue background
4. **All forms work** - try submitting to see alerts
5. **Responsive** - resize browser to see mobile sidebar

## 💡 Key JavaScript Functions

### Navigation
- `setActiveSidebarLink()` - Highlights current page
- `initMobileSidebar()` - Mobile menu toggle
- `handleLogout()` - Logout with confirmation

### Dashboard
- `loadDashboard()` - Loads all dashboard data
- `loadTeacherInfo()` - Shows teacher profile
- `loadDashboardStats()` - Displays stats cards
- `loadRecentActivity()` - Recent activity feed

### Page-Specific
- `loadRoutine()` - Weekly schedule
- `loadCourseMaterials()` - Course materials table
- `loadAssignments()` - Assignments table
- `loadResults()` - Student results & summary
- `loadAttendance()` - Attendance records
- `loadNotices()` - Noticeboard items
- `loadProfile()` - Teacher profile

## 📱 Responsive Design

### Desktop (>968px)
- Sidebar visible on left
- Full-width content area
- Multi-column layouts

### Tablet & Mobile (<968px)
- Sidebar hidden by default
- Hamburger menu button appears
- Tap to show/hide sidebar
- Single column layouts
- Touch-friendly buttons

## 🎨 Customization

### Change Colors
Edit CSS variables in `style.css`:
```css
:root {
  --primary: #1E90FF;        /* Main blue color */
  --sidebar-bg: #1E90FF;     /* Sidebar background */
  --sidebar-active: #1873CC; /* Active link */
}
```

### Update Teacher Data
Edit `teacherData` object in `script.js`:
```javascript
const teacherData = {
  name: 'Your Name',
  subject: 'Your Subject',
  // ... other fields
};
```

### Modify Students
Edit `studentsData` array in `script.js`

## ✨ Special Features

- **Smooth animations** on page load
- **Hover effects** on all interactive elements
- **Color-coded badges** for status (Active, Completed, Graded)
- **Gradient headers** on tables
- **Shadow effects** on cards for depth
- **Mobile-optimized** sidebar with overlay
- **Professional typography** with Poppins font
- **Consistent spacing** throughout

## 🔧 Browser Compatibility

- ✅ Chrome/Edge (Latest)
- ✅ Firefox (Latest)
- ✅ Safari (Latest)
- ✅ Mobile browsers

---

**Built with 💙 for teachers to efficiently manage their classes and students!**
