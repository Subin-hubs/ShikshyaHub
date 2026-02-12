/* ============================================================
   STUDENT PORTAL — script.js
   All placeholder data + dynamic rendering + nav logic
   ============================================================ */

/* ──────────────────────────────
   STUDENT DATA
────────────────────────────── */
const student = {
  name:       "Aiden Carter",
  id:         "STU-2024-0847",
  dept:       "Computer Science & Engineering",
  semester:   "Semester V",
  year:       "3rd Year · 2022–2026",
  cgpa:       "3.72",
  sgpa:       "3.81",
  credits:    72,
  avatar:     "AC"
};

/* ──────────────────────────────
   COURSES DATA
────────────────────────────── */
const courses = [
  {
    code: "CS501", emoji: "🧩", bg: "#EEF2FF",
    title: "Data Structures & Algorithms",
    instructor: "Prof. Sarah Mitchell",
    credits: 4, schedule: "Mon / Wed / Fri",
    time: "9:00 AM", room: "CSE Lab 3",
    progress: 74, status: "ongoing"
  },
  {
    code: "CS502", emoji: "⚙️", bg: "#F0FDF4",
    title: "Operating Systems",
    instructor: "Prof. James Turner",
    credits: 4, schedule: "Tue / Thu",
    time: "10:30 AM", room: "Block B · 204",
    progress: 62, status: "ongoing"
  },
  {
    code: "CS503", emoji: "🗄️", bg: "#FFF7ED",
    title: "Database Management Systems",
    instructor: "Prof. Linda Chen",
    credits: 3, schedule: "Mon / Wed",
    time: "2:00 PM", room: "Block A · 108",
    progress: 81, status: "ongoing"
  },
  {
    code: "CS504", emoji: "🌐", bg: "#F0FDFA",
    title: "Computer Networks",
    instructor: "Prof. Robert Evans",
    credits: 3, schedule: "Tue / Thu / Fri",
    time: "11:00 AM", room: "Block C · 302",
    progress: 55, status: "ongoing"
  },
  {
    code: "MA501", emoji: "📊", bg: "#FEFCE8",
    title: "Probability & Statistics",
    instructor: "Prof. Anna Simmons",
    credits: 3, schedule: "Mon / Wed / Fri",
    time: "1:00 PM", room: "Math Block · 101",
    progress: 89, status: "ongoing"
  },
  {
    code: "HU501", emoji: "✍️", bg: "#FFF1F2",
    title: "Technical Communication",
    instructor: "Prof. David Park",
    credits: 2, schedule: "Tue",
    time: "3:30 PM", room: "Block A · 210",
    progress: 92, status: "ongoing"
  }
];

/* ──────────────────────────────
   RESULTS DATA
────────────────────────────── */
const results = {
  current: "Semester V (Oct 2024 – Feb 2025)",
  sgpa: "3.81",
  cgpa: "3.72",
  credits: 19,
  subjects: [
    { emoji:"🧩", code:"CS501", title:"Data Structures & Algorithms", credits:4, internal:38, external:72, total:110, max:125, grade:"A",  gp:4.0, remarks:"Excellent" },
    { emoji:"⚙️", code:"CS502", title:"Operating Systems",            credits:4, internal:35, external:68, total:103, max:125, grade:"A-", gp:3.7, remarks:"Very Good" },
    { emoji:"🗄️", code:"CS503", title:"Database Management Systems",  credits:3, internal:40, external:74, total:114, max:125, grade:"A",  gp:4.0, remarks:"Excellent" },
    { emoji:"🌐", code:"CS504", title:"Computer Networks",            credits:3, internal:33, external:64, total:97,  max:125, grade:"B+", gp:3.3, remarks:"Good" },
    { emoji:"📊", code:"MA501", title:"Probability & Statistics",     credits:3, internal:37, external:70, total:107, max:125, grade:"A-", gp:3.7, remarks:"Very Good" },
    { emoji:"✍️", code:"HU501", title:"Technical Communication",      credits:2, internal:40, external:75, total:115, max:125, grade:"A",  gp:4.0, remarks:"Excellent" }
  ],
  history: [
    { sem:"Semester IV", sgpa:"3.60", cgpa:"3.65", credits:20, status:"Passed" },
    { sem:"Semester III", sgpa:"3.55", cgpa:"3.68", credits:18, status:"Passed" },
    { sem:"Semester II", sgpa:"3.70", cgpa:"3.72", credits:18, status:"Passed" },
    { sem:"Semester I",  sgpa:"3.50", cgpa:"3.50", credits:16, status:"Passed" }
  ]
};

/* ──────────────────────────────
   ASSIGNMENTS DATA
────────────────────────────── */
const assignments = {
  pending: [
    { title:"Binary Search Tree Implementation", course:"CS501 · DSA",         due:"Feb 18, 2025", daysLeft:6,  priority:"high" },
    { title:"Process Scheduling Simulation",     course:"CS502 · OS",           due:"Feb 20, 2025", daysLeft:8,  priority:"medium" },
    { title:"ER Diagram & Normalization Report", course:"CS503 · DBMS",         due:"Feb 22, 2025", daysLeft:10, priority:"medium" },
    { title:"Network Topology Design",           course:"CS504 · Networks",     due:"Feb 25, 2025", daysLeft:13, priority:"low" },
    { title:"Technical Report Writing",          course:"HU501 · TechComm",     due:"Feb 28, 2025", daysLeft:16, priority:"low" }
  ],
  submitted: [
    { title:"Array & Linked List Operations",   course:"CS501 · DSA",     submittedOn:"Jan 30, 2025", score:"47/50", status:"Graded" },
    { title:"Shell Script Programming",         course:"CS502 · OS",      submittedOn:"Feb 02, 2025", score:"44/50", status:"Graded" },
    { title:"SQL Queries & Joins",              course:"CS503 · DBMS",    submittedOn:"Feb 05, 2025", score:"48/50", status:"Graded" },
    { title:"Statistics Problem Set 1",         course:"MA501 · Stats",   submittedOn:"Feb 10, 2025", score:"—",     status:"Under Review" },
    { title:"OSI vs TCP/IP Essay",              course:"CS504 · Networks", submittedOn:"Feb 12, 2025", score:"—",     status:"Submitted" }
  ]
};

/* ──────────────────────────────
   ATTENDANCE DATA
────────────────────────────── */
const attendance = [
  { code:"CS501", title:"Data Structures & Algorithms", total:45, present:38, absent:7,  pct:84 },
  { code:"CS502", title:"Operating Systems",            total:30, present:24, absent:6,  pct:80 },
  { code:"CS503", title:"Database Management Systems",  total:30, present:28, absent:2,  pct:93 },
  { code:"CS504", title:"Computer Networks",            total:45, present:32, absent:13, pct:71 },
  { code:"MA501", title:"Probability & Statistics",     total:45, present:43, absent:2,  pct:96 },
  { code:"HU501", title:"Technical Communication",      total:15, present:14, absent:1,  pct:93 }
];

/* ──────────────────────────────
   NOTICES DATA
────────────────────────────── */
const notices = [
  { type:"important", dot:"dot-rose",   icon:"📢", category:"Exam",       date:"Feb 10, 2025", by:"Academic Office",         title:"Mid-Semester Exam Schedule Released",   body:"Examinations will be held from March 10–20, 2025. Check the exam portal for your detailed schedule and report discrepancies to the Academic Office by Feb 16." },
  { type:"important", dot:"dot-rose",   icon:"⚠️", category:"Finance",    date:"Feb 09, 2025", by:"Finance Department",      title:"Fee Payment Deadline – March 5, 2025",  body:"All students must clear their outstanding fee balance by March 5, 2025. Late fee penalty of ₹500/week applies after the due date." },
  { type:"announce",  dot:"dot-indigo", icon:"🏆", category:"Event",      date:"Feb 08, 2025", by:"Student Activities Board", title:"TechFest 2025 – Registrations Open",    body:"Annual Technical Festival from Feb 28 – Mar 2. Events: Hackathon, Coding Sprint, Robotics, Paper Presentation. Register on the Student Activities Portal." },
  { type:"general",   dot:"dot-teal",   icon:"📚", category:"Academic",   date:"Feb 07, 2025", by:"Library Administration",  title:"Library Timings Extended for Exam Season", body:"Central Library open until 11:00 PM from February 20. Study rooms available online. ID cards mandatory for entry." },
  { type:"general",   dot:"dot-teal",   icon:"💡", category:"Workshop",   date:"Feb 06, 2025", by:"CSE Department",           title:"Workshop on Cloud Computing – Feb 22",  body:"One-day workshop on Cloud Computing & DevOps by AWS experts. Free but registration mandatory. Limited seats—register before Feb 18." },
  { type:"announce",  dot:"dot-indigo", icon:"💼", category:"Placement",  date:"Feb 05, 2025", by:"Training & Placement Cell", title:"Campus Placement – Infosys & Wipro",   body:"Placement drives for Infosys and Wipro Technologies scheduled March 15–16. Eligibility: CGPA ≥ 3.5, no active backlogs. Register on Placement Portal by Feb 25." }
];

/* ──────────────────────────────
   FEES DATA
────────────────────────────── */
const fees = {
  total:    185000,
  paid:     140000,
  due:      45000,
  dueDate:  "March 5, 2025",
  semester: "Semester V",
  history: [
    { inv:"INV-2024-1201", date:"Oct 01, 2024", desc:"Tuition Fee – Sem V (Part 1)",        amount:60000, mode:"Online Transfer", status:"Paid" },
    { inv:"INV-2024-1089", date:"Aug 15, 2024", desc:"Hostel Fee – Academic Year 2024–25",  amount:48000, mode:"Demand Draft",    status:"Paid" },
    { inv:"INV-2024-1050", date:"Jul 20, 2024", desc:"Library & Lab Fee – Annual",          amount:12000, mode:"Online Transfer", status:"Paid" },
    { inv:"INV-2024-0920", date:"Jun 30, 2024", desc:"Development & Activity Fee",          amount:8000,  mode:"Credit Card",     status:"Paid" },
    { inv:"INV-2025-0101", date:"Jan 05, 2025", desc:"Tuition Fee – Sem V (Part 2)",        amount:12000, mode:"Online Transfer", status:"Paid" },
    { inv:"INV-2025-0201", date:"Mar 05, 2025", desc:"Tuition Fee – Sem V (Final Installment)", amount:45000, mode:"—",           status:"Pending" }
  ]
};

/* ============================================================
   HELPERS
   ============================================================ */
const INR = n => "₹" + n.toLocaleString("en-IN");

function pctColor(p) {
  if (p >= 85) return "green";
  if (p >= 75) return "amber";
  return "rose";
}

function gradeColor(g) {
  if (g.startsWith("A")) return "badge-green";
  if (g.startsWith("B")) return "badge-indigo";
  return "badge-amber";
}

function priorityBadge(p) {
  const map = { high:"badge-rose", medium:"badge-amber", low:"badge-slate" };
  return `<span class="badge ${map[p]}">${p.charAt(0).toUpperCase()+p.slice(1)}</span>`;
}

function statusBadge(s) {
  const map = { "Graded":"badge-green", "Under Review":"badge-amber", "Submitted":"badge-indigo", "Pending":"badge-rose", "Paid":"badge-green" };
  return `<span class="badge ${map[s] || 'badge-slate'}">${s}</span>`;
}

/* ============================================================
   RENDER — DASHBOARD
   ============================================================ */
function renderDashboard() {
  /* Info strip */
  const di = document.getElementById("dashboard-info");
  if (di) {
    di.innerHTML = `
      <div class="welcome-banner">
        <div class="welcome-text">
          <h2>Good morning, ${student.name.split(" ")[0]}! 👋</h2>
          <p>${student.dept} &middot; ${student.semester} &middot; ${student.year}</p>
        </div>
        <div class="welcome-meta">
          <div class="welcome-stat">
            <div class="welcome-stat-val">${student.cgpa}</div>
            <div class="welcome-stat-lbl">CGPA</div>
          </div>
          <div class="welcome-stat">
            <div class="welcome-stat-val">${courses.length}</div>
            <div class="welcome-stat-lbl">Courses</div>
          </div>
          <div class="welcome-stat">
            <div class="welcome-stat-val">${assignments.pending.length}</div>
            <div class="welcome-stat-lbl">Pending</div>
          </div>
        </div>
      </div>`;
  }

  /* Stat cards */
  const dc = document.getElementById("dashboard-cards");
  if (dc) {
    const paidPct = Math.round((fees.paid / fees.total) * 100);
    dc.innerHTML = `
      <div class="stat-card indigo">
        <div class="stat-icon indigo"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/></svg></div>
        <div class="stat-value">${courses.length}</div>
        <div class="stat-label">Enrolled Courses</div>
        <span class="stat-sub neutral">Semester V</span>
      </div>
      <div class="stat-card teal">
        <div class="stat-icon teal"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg></div>
        <div class="stat-value">${assignments.pending.length}</div>
        <div class="stat-label">Pending Assignments</div>
        <span class="stat-sub warn">${assignments.submitted.length} submitted</span>
      </div>
      <div class="stat-card amber">
        <div class="stat-icon amber"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg></div>
        <div class="stat-value">${results.sgpa}</div>
        <div class="stat-label">Current SGPA</div>
        <span class="stat-sub good">CGPA ${results.cgpa}</span>
      </div>
      <div class="stat-card rose">
        <div class="stat-icon rose"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>
        <div class="stat-value">${paidPct}%</div>
        <div class="stat-label">Fees Paid</div>
        <span class="stat-sub warn">${INR(fees.due)} due</span>
      </div>`;
  }

  /* Upcoming assignments */
  const ua = document.getElementById("upcoming-assignments");
  if (ua) {
    ua.innerHTML = assignments.pending.slice(0, 4).map(a => `
      <div class="assign-item">
        <div>
          <div class="assign-title">${a.title}</div>
          <div class="assign-course">${a.course}</div>
        </div>
        <div class="assign-right">
          <span class="assign-due">${a.due}</span>
          <span class="badge ${a.daysLeft <= 7 ? "badge-rose" : a.daysLeft <= 10 ? "badge-amber" : "badge-slate"}">${a.daysLeft}d left</span>
        </div>
      </div>`).join("");
  }

  /* Recent notices */
  const rn = document.getElementById("recent-notices");
  if (rn) {
    rn.innerHTML = notices.slice(0, 4).map(n => `
      <div class="notice-item">
        <div class="notice-dot ${n.dot}"></div>
        <div style="flex:1">
          <div class="notice-title">${n.title}</div>
          <div class="notice-meta">
            <span>${n.date}</span>
            <span>·</span>
            <span>${n.by}</span>
          </div>
        </div>
        <span class="badge ${n.type === "important" ? "badge-rose" : n.type === "announce" ? "badge-indigo" : "badge-teal"}">${n.category}</span>
      </div>`).join("");
  }
}

/* ============================================================
   RENDER — COURSES
   ============================================================ */
function renderCourses() {
  const cc = document.getElementById("courses-container");
  if (!cc) return;

  const pColor = (p) => p >= 80 ? "green" : p >= 60 ? "indigo" : "rose";

  cc.innerHTML = `<div class="courses-grid">${courses.map(c => `
    <div class="course-card">
      <div class="course-top">
        <div class="course-emoji" style="background:${c.bg}">${c.emoji}</div>
        <span class="badge badge-indigo">${c.credits} Credits</span>
      </div>
      <div class="course-code">${c.code}</div>
      <div class="course-title">${c.title}</div>
      <div class="course-instructor">
        <svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
        ${c.instructor}
      </div>
      <div class="course-chips">
        <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>${c.schedule}</span>
        <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>${c.time}</span>
        <span class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>${c.room}</span>
      </div>
      <div class="progress-labels">
        <span>Progress</span>
        <span>${c.progress}%</span>
      </div>
      <div class="progress-wrap"><div class="progress-fill ${pColor(c.progress)}" style="width:${c.progress}%"></div></div>
    </div>`).join("")}</div>`;
}

/* ============================================================
   RENDER — RESULTS
   ============================================================ */
function renderResults() {
  const rs = document.getElementById("results-summary");
  if (rs) {
    rs.innerHTML = `
      <div class="gpa-grid">
        <div class="gpa-card primary">
          <div class="gpa-val">${results.sgpa}</div>
          <div class="gpa-lbl">SGPA</div>
          <div class="gpa-sub">Current Semester</div>
        </div>
        <div class="gpa-card">
          <div class="gpa-val">${results.cgpa}</div>
          <div class="gpa-lbl">CGPA</div>
          <div class="gpa-sub">Cumulative</div>
        </div>
        <div class="gpa-card">
          <div class="gpa-val">${results.credits}</div>
          <div class="gpa-lbl">Credits</div>
          <div class="gpa-sub">This Semester</div>
        </div>
      </div>`;
  }

  const rt = document.getElementById("results-table");
  if (rt) {
    rt.innerHTML = `
      <div class="card mb-24">
        <div class="card-header">
          <h2>
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            ${results.current}
          </h2>
        </div>
        <div class="card-body" style="padding:0">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Code</th>
                  <th>Credits</th>
                  <th>Internal</th>
                  <th>External</th>
                  <th>Total / 125</th>
                  <th>Grade</th>
                  <th>GP</th>
                  <th>Remarks</th>
                </tr>
              </thead>
              <tbody>
                ${results.subjects.map(s => `
                  <tr>
                    <td><span style="font-size:16px;margin-right:8px">${s.emoji}</span><span class="td-main">${s.title}</span></td>
                    <td class="text-muted">${s.code}</td>
                    <td>${s.credits}</td>
                    <td>${s.internal}</td>
                    <td>${s.external}</td>
                    <td class="fw-600">${s.total}</td>
                    <td><span class="badge ${gradeColor(s.grade)}">${s.grade}</span></td>
                    <td class="fw-700 text-indigo">${s.gp.toFixed(1)}</td>
                    <td>${s.remarks}</td>
                  </tr>`).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h2>
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            Previous Semesters
          </h2>
        </div>
        <div class="card-body" style="padding:0">
          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>Semester</th><th>SGPA</th><th>CGPA</th><th>Credits</th><th>Status</th></tr>
              </thead>
              <tbody>
                ${results.history.map(h => `
                  <tr>
                    <td class="td-main">${h.sem}</td>
                    <td class="fw-700 text-indigo">${h.sgpa}</td>
                    <td class="fw-600">${h.cgpa}</td>
                    <td>${h.credits}</td>
                    <td>${statusBadge(h.status)}</td>
                  </tr>`).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>`;
  }
}

/* ============================================================
   RENDER — ASSIGNMENTS
   ============================================================ */
function renderAssignments() {
  const at = document.getElementById("assignments-table");
  if (!at) return;

  at.innerHTML = `
    <div class="card mb-24">
      <div class="card-header">
        <h2>
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Pending Assignments
        </h2>
        <span class="badge badge-rose">${assignments.pending.length} pending</span>
      </div>
      <div class="card-body" style="padding:0">
        <div class="table-wrap">
          <table>
            <thead>
              <tr><th>Assignment</th><th>Course</th><th>Due Date</th><th>Days Left</th><th>Priority</th></tr>
            </thead>
            <tbody>
              ${assignments.pending.map(a => `
                <tr>
                  <td class="td-main">${a.title}</td>
                  <td><span class="badge badge-indigo">${a.course.split(" · ")[0]}</span></td>
                  <td class="text-muted">${a.due}</td>
                  <td>
                    <span class="badge ${a.daysLeft <= 7 ? "badge-rose" : a.daysLeft <= 10 ? "badge-amber" : "badge-slate"}">${a.daysLeft} days</span>
                  </td>
                  <td>${priorityBadge(a.priority)}</td>
                </tr>`).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Submitted Assignments
        </h2>
        <span class="badge badge-green">${assignments.submitted.length} submitted</span>
      </div>
      <div class="card-body" style="padding:0">
        <div class="table-wrap">
          <table>
            <thead>
              <tr><th>Assignment</th><th>Course</th><th>Submitted On</th><th>Score</th><th>Status</th></tr>
            </thead>
            <tbody>
              ${assignments.submitted.map(a => `
                <tr>
                  <td class="td-main">${a.title}</td>
                  <td><span class="badge badge-indigo">${a.course.split(" · ")[0]}</span></td>
                  <td class="text-muted">${a.submittedOn}</td>
                  <td class="fw-600 ${a.score !== "—" ? "text-green" : "text-muted"}">${a.score}</td>
                  <td>${statusBadge(a.status)}</td>
                </tr>`).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>`;
}

/* ============================================================
   RENDER — ATTENDANCE
   ============================================================ */
function renderAttendance() {
  const at = document.getElementById("attendance-table");
  if (!at) return;

  const overall = Math.round(attendance.reduce((s, c) => s + c.pct, 0) / attendance.length);
  const pColor = pctColor;

  at.innerHTML = `
    <!-- Mini cards overview -->
    <div class="att-overview mb-24">
      ${attendance.map(a => `
        <div class="att-mini">
          <div class="att-circle ${pColor(a.pct)}">${a.pct}%</div>
          <div class="att-mini-course">${a.code}</div>
          <div class="att-mini-sub">${a.title.split(" ").slice(0,2).join(" ")}</div>
        </div>`).join("")}
    </div>

    <!-- Detail table -->
    <div class="card">
      <div class="card-header">
        <h2>
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/></svg>
          Detailed Attendance Report
        </h2>
        <span class="badge ${pColor(overall) === "green" ? "badge-green" : pColor(overall) === "amber" ? "badge-amber" : "badge-rose"}">Overall: ${overall}%</span>
      </div>
      <div class="card-body" style="padding:0">
        <div class="table-wrap">
          <table>
            <thead>
              <tr><th>Course</th><th>Code</th><th>Total Classes</th><th>Attended</th><th>Absent</th><th>Attendance %</th><th>Status</th></tr>
            </thead>
            <tbody>
              ${attendance.map(a => `
                <tr>
                  <td class="td-main">${a.title}</td>
                  <td class="text-muted">${a.code}</td>
                  <td>${a.total}</td>
                  <td class="fw-600 text-green">${a.present}</td>
                  <td class="fw-600 text-rose">${a.absent}</td>
                  <td>
                    <div style="display:flex;align-items:center;gap:10px;min-width:140px">
                      <div class="progress-wrap" style="flex:1;margin:0"><div class="progress-fill ${pColor(a.pct)}" style="width:${a.pct}%"></div></div>
                      <span class="fw-700 ${pColor(a.pct) === "green" ? "text-green" : pColor(a.pct) === "amber" ? "text-amber" : "text-rose"}">${a.pct}%</span>
                    </div>
                  </td>
                  <td>
                    <span class="badge ${a.pct >= 85 ? "badge-green" : a.pct >= 75 ? "badge-amber" : "badge-rose"}">
                      ${a.pct >= 85 ? "Safe" : a.pct >= 75 ? "Warning" : "At Risk"}
                    </span>
                  </td>
                </tr>`).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Note -->
    <div style="margin-top:16px;padding:14px 18px;background:var(--amber-light);border-radius:var(--radius);border:1px solid #FDE68A;font-size:13px;color:#92400E;">
      ⚠️ <strong>Note:</strong> Minimum 75% attendance is required to be eligible for examinations. Students with attendance below 75% must apply for attendance condonation at the Academic Office.
    </div>`;
}

/* ============================================================
   RENDER — NOTICE BOARD
   ============================================================ */
function renderNotices() {
  const nl = document.getElementById("notice-list");
  if (!nl) return;

  nl.innerHTML = `
    <!-- Filter buttons -->
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px" id="notice-filters">
      <button class="notice-filter-btn active" data-filter="all">All</button>
      <button class="notice-filter-btn" data-filter="important">🔴 Important</button>
      <button class="notice-filter-btn" data-filter="announce">🔵 Announcements</button>
      <button class="notice-filter-btn" data-filter="general">🟢 General</button>
    </div>

    <style>
      .notice-filter-btn {
        padding: 6px 16px;
        border-radius: 99px;
        border: 1px solid var(--slate-200);
        background: var(--white);
        font-size: 12px;
        font-weight: 600;
        color: var(--slate-500);
        cursor: pointer;
        font-family: var(--font);
        transition: all .15s;
      }
      .notice-filter-btn.active, .notice-filter-btn:hover {
        background: var(--indigo);
        color: white;
        border-color: var(--indigo);
      }
      .notice-full-card {
        background: var(--white);
        border: 1px solid var(--slate-200);
        border-radius: var(--radius-lg);
        padding: 20px 22px;
        margin-bottom: 14px;
        display: flex;
        gap: 16px;
        transition: box-shadow .2s;
      }
      .notice-full-card:hover { box-shadow: var(--shadow-sm); }
      .notice-full-card.important { border-left: 4px solid var(--rose); }
      .notice-full-card.announce  { border-left: 4px solid var(--indigo); }
      .notice-full-card.general   { border-left: 4px solid var(--teal); }
      .notice-icon-box {
        width: 44px; height: 44px;
        border-radius: var(--radius);
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; flex-shrink: 0;
      }
      .notice-full-card.important .notice-icon-box { background: var(--rose-light); }
      .notice-full-card.announce  .notice-icon-box { background: var(--indigo-light); }
      .notice-full-card.general   .notice-icon-box { background: var(--teal-light); }
      .notice-body-text { font-size: 13.5px; color: var(--slate-600); line-height: 1.6; margin-bottom: 10px; }
    </style>

    <div id="notices-output">
      ${notices.map(n => `
        <div class="notice-full-card ${n.type}" data-type="${n.type}">
          <div class="notice-icon-box">${n.icon}</div>
          <div style="flex:1">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:6px;flex-wrap:wrap">
              <div class="notice-title" style="font-size:15px">${n.title}</div>
              <span class="badge ${n.type === "important" ? "badge-rose" : n.type === "announce" ? "badge-indigo" : "badge-teal"}">${n.category}</span>
            </div>
            <div class="notice-body-text">${n.body}</div>
            <div class="notice-meta">
              <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
              ${n.date}
              <span>·</span>
              <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              ${n.by}
            </div>
          </div>
        </div>`).join("")}
    </div>`;

  /* Filter logic */
  setTimeout(() => {
    document.querySelectorAll(".notice-filter-btn").forEach(btn => {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".notice-filter-btn").forEach(b => b.classList.remove("active"));
        this.classList.add("active");
        const f = this.dataset.filter;
        document.querySelectorAll(".notice-full-card").forEach(card => {
          card.style.display = (f === "all" || card.dataset.type === f) ? "" : "none";
        });
      });
    });
  }, 0);
}

/* ============================================================
   RENDER — FEES
   ============================================================ */
function renderFees() {
  const pct = Math.round((fees.paid / fees.total) * 100);

  const fs = document.getElementById("fee-status");
  if (fs) {
    fs.innerHTML = `
      <div class="fees-overview">
        <div class="fee-card">
          <div class="fee-lbl">Total Fees</div>
          <div class="fee-amount">${INR(fees.total)}</div>
          <div class="fee-sub">${fees.semester}</div>
        </div>
        <div class="fee-card primary">
          <div class="fee-lbl">Amount Paid</div>
          <div class="fee-amount">${INR(fees.paid)}</div>
          <div class="fee-sub">${pct}% of total fees</div>
          <div class="fee-bar-outer"><div class="fee-bar-inner" style="width:${pct}%"></div></div>
        </div>
        <div class="fee-card" style="border-color:var(--rose)">
          <div class="fee-lbl">Balance Due</div>
          <div class="fee-amount" style="color:var(--rose)">${INR(fees.due)}</div>
          <div class="fee-sub" style="color:var(--rose)">Due by ${fees.dueDate}</div>
        </div>
      </div>

      <div class="payment-alert">
        <div class="alert-left">
          <div class="alert-icon">⏰</div>
          <div>
            <div class="alert-title">Upcoming Payment Due</div>
            <div class="alert-desc">Your next installment of <strong>${INR(fees.due)}</strong> is due on <strong>${fees.dueDate}</strong>. Pay on time to avoid penalties.</div>
          </div>
        </div>
        <button class="btn-pay" onclick="alert('Redirecting to payment gateway…')">Pay Now →</button>
      </div>`;
  }

  const fh = document.getElementById("fee-history");
  if (fh) {
    fh.innerHTML = `
      <div class="card">
        <div class="card-header">
          <h2>
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            Payment History
          </h2>
        </div>
        <div class="card-body" style="padding:0">
          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>Invoice No.</th><th>Date</th><th>Description</th><th>Amount</th><th>Mode</th><th>Status</th></tr>
              </thead>
              <tbody>
                ${fees.history.map(h => `
                  <tr>
                    <td class="fw-600 text-indigo">${h.inv}</td>
                    <td class="text-muted">${h.date}</td>
                    <td class="td-main">${h.desc}</td>
                    <td class="fw-700">${INR(h.amount)}</td>
                    <td class="text-muted">${h.mode}</td>
                    <td>${statusBadge(h.status)}</td>
                  </tr>`).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>`;
  }
}

/* ============================================================
   NAVBAR — Mobile Toggle + Logout
   ============================================================ */
function initNavbar() {
  /* Mobile hamburger */
  const ham = document.getElementById("nav-hamburger");
  const mobileNav = document.getElementById("mobile-nav");
  if (ham && mobileNav) {
    ham.addEventListener("click", () => mobileNav.classList.toggle("open"));
  }

  /* Close mobile nav on link click */
  document.querySelectorAll(".mobile-nav .nav-link").forEach(link => {
    link.addEventListener("click", () => mobileNav && mobileNav.classList.remove("open"));
  });

  /* Logout */
  document.querySelectorAll(".logout-trigger").forEach(btn => {
    btn.addEventListener("click", () => {
      if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("student_session");
        sessionStorage.clear();
        window.location.href = "login.html";
      }
    });
  });
}

/* ============================================================
   INIT — run the right renderer per page
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  initNavbar();

  const page = document.body.dataset.page;
  const renderers = {
    dashboard:   renderDashboard,
    courses:     renderCourses,
    results:     renderResults,
    assignments: renderAssignments,
    attendance:  renderAttendance,
    noticeboard: renderNotices,
    fees:        renderFees
  };

  if (renderers[page]) renderers[page]();
});
