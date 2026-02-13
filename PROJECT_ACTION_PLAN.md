# ShikshyaHub: Recommended Next Steps

## Current Assessment

The project has a strong base (Flask app factory, role-based blueprints, SQLAlchemy models), but there are a few blockers that should be resolved before adding new features.

## Priority Plan

### 1) Stabilize core navigation and templates (Highest)
- Fix route/template mismatches that currently risk runtime `TemplateNotFound` errors:
  - `main.py` references `public/about.html` and `public/contact.html`, but only `public/home.html` exists.
  - `auth.py` returns `auth/login.html`, but no `auth/` template file exists.
  - `student.py` references `student/grades.html` and `student/notices.html`, while existing files are `student/results.html` and `student/noticeboard.html`.
  - `teacher.py` references `teacher/grades.html`, while existing file is `teacher/results.html`.
- Standardize naming conventions across routes/templates (`results` vs `grades`, `noticeboard` vs `notices`, `course` vs `courses`).

### 2) Correct route path definitions (High)
- Add missing leading `/` in multiple student routes (`attendance`, `grades`, `notices`, `assignments`) so URL rules are explicit and consistent.
- Normalize API endpoint prefixes inside blueprints (avoid duplicated `/student/...` inside a blueprint already using `url_prefix='/student'`).

### 3) Clean up duplicated and inconsistent backend logic (High)
- In `admin.py`, remove duplicated code blocks (e.g., repeated `add_course` logic appearing after an early return path).
- Move role checks (`check_admin`, `current_user.role` checks) into reusable decorators/helpers to avoid drift.

### 4) Protect data integrity and security (High)
- Restrict open registration or add role-safe onboarding (currently role is selected directly from user input in registration flow).
- Add server-side validation with WTForms (or equivalent) to all form/API payloads.
- Add CSRF protection checks for state-changing endpoints and validate file uploads strictly.

### 5) Add migrations and environment setup hardening (Medium)
- Introduce `Flask-Migrate` for schema evolution (currently no migration workflow documented).
- Add `.env.example`, setup steps, and a proper quickstart in `README.md`.
- Ensure `instance/shikshyahub.db` is excluded from source control for production hygiene.

### 6) Add tests before feature expansion (Medium)
- Start with smoke tests:
  - auth login/logout
  - role-based dashboard access
  - critical API endpoints (course add/enroll/attendance)
- Then add integration tests for common user journeys (admin creates course, teacher marks attendance, student views results).

## Suggested 2-Week Execution Sequence
1. **Week 1:** route/template fixes + naming standardization + admin cleanup.
2. **Week 2:** registration/validation hardening + migrations + test suite bootstrap.

## Outcome
After these steps, ShikshyaHub will be much more stable and easier to extend safely with new modules (fees, analytics, notices, parent portal, etc.).
