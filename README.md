# Manicks Recruitment Services Job Portal

A production-minded Django job portal starter built for learning and real-world growth. It uses Django templates first, keeps the code modular, and stays friendly to low-cost hosting.

## What this project includes
- Custom user model with `job_seeker`, `recruiter`, and `admin` roles
- Separate profiles for job seekers and recruiters
- Company profile management
- Job posting, editing, closing, search, filtering, and pagination
- Job applications with status tracking
- Recruiter applicant review flow
- Django admin for portal management
- DRF API skeleton for jobs and logged-in applications
- Sample data command and automated tests

## Recommended local setup
1. Open PowerShell in the project folder.
2. Create a virtual environment if you do not already have one:
   ```powershell
   python -m venv .venv
   ```
3. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Copy the environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
6. Run migrations:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Seed demo data:
   ```powershell
   python manage.py seed_portal
   ```
8. Start the server:
   ```powershell
   python manage.py runserver
   ```
9. Open `http://127.0.0.1:8000/`.

## Demo users after seeding
- Admin: `adminuser` / `AdminPass123!`
- Recruiter: `recruiter1` / `RecruiterPass123!`
- Job seeker: `seeker1` / `SeekerPass123!`

## Project structure
- `config/`: project settings, URLs, ASGI, WSGI
- `apps/core/`: shared base models, home page, error handling, seed command
- `apps/accounts/`: custom user, profiles, auth flows, dashboards
- `apps/companies/`: recruiter company profiles
- `apps/jobs/`: skills, job posts, search, filtering
- `apps/applications/`: job applications and status workflow
- `apps/api/`: starter REST API endpoints
- `templates/`: shared and app templates
- `static/`: CSS and frontend assets
- `media/`: uploaded files in local development

## How to test locally
- Run all tests:
  ```powershell
  python manage.py test
  ```
- Run one app only:
  ```powershell
  python manage.py test apps.jobs
  ```
- Check for configuration issues:
  ```powershell
  python manage.py check
  ```

## How to debug errors
- Read the first line in your own file inside the traceback. That is usually where the real bug starts.
- If models changed, run `makemigrations` and `migrate`.
- If a page cannot be found, check the URL name in `urls.py` and in the template.
- If a template is missing, confirm the path matches the app and filename exactly.
- If a file upload fails, check `MEDIA_ROOT`, `MEDIA_URL`, and the form `enctype`.
- Use Django admin and `python manage.py shell` to inspect saved data directly.

## Common beginner mistakes this project avoids
- Starting without a custom user model
- Mixing recruiter and seeker fields in one profile table
- Writing all logic in views instead of separating selectors and services
- Hard deleting jobs instead of closing them
- Forgetting permission checks on recruiter-only and seeker-only pages
- Building for SQLite in a way that blocks PostgreSQL later

## Future upgrade path
- Switch the database from SQLite to PostgreSQL in `config/settings/production.py`
- Add Redis for caching, task queues, or rate limiting later
- Replace local media storage with object storage later
- Expand DRF endpoints and add JWT when mobile or React clients need it
- Move frontend pages to React or Next.js while keeping the Django domain logic
- Add multi-tenant company accounts after the single-portal workflow is stable
