# Voting Platform

A simple Flask web application for voting, built with **Flask + SQLAlchemy**, using **PostgreSQL** by default and containerized with **Docker Compose**. It includes user accounts, candidate management, and live results.

## Features
- **Auth**: Register/Login; session-based auth  
- **One vote per user**: Enforced server-side  
- **Admin panel**: Add candidates, view stats  
- **Live results**: Progress bars and totals  
- **PostgreSQL**: Primary database (via Docker)  
- **Migrations**: Alembic/Flask-Migrate for schema changes  
- **Docker dev UX**: Hot-reload (bind mount + `flask run --reload`)  
- **Seeding**: Idempotent default users/candidates on startup

> Passwords are stored **hashed** (bcrypt). Sample passwords are only for local development.
## Tech Stack
- **Backend**: Python 3.11, Flask, SQLAlchemy  
- **DB**: PostgreSQL (Docker)  
- **Migrations**: Alembic via Flask-Migrate  
- **Frontend**: Jinja2 templates, Bootstrap 5  
- **Containers**: Docker + Docker Compose

## Quick Start (Docker – Recommended)

### 1) Clone and enter the project folder
```bash
git clone https://github.com/RMITSSD/ssd-assignment3-voter-registration.git
cd ssd-assignment3-voter-registration
FLASK_APP=app:create_app
FLASK_DEBUG=1
SECRET_KEY=dev-change-me
### 2) Create your .env (required, repo root)
# Used for native runs; inside containers the host is overridden to `db`
DATABASE_URL=postgresql://voting_user:voting_password@localhost:5432/voting_db
docker compose up --build
### 3) Start services (db → migrate+seed → web)

Option A (one command, shows logs)

docker compose up --build


Option B (step-by-step)

docker compose up -d db
docker compose run --rm migrate     # applies migrations & seeds data once
docker compose up web               # starts Flask with hot-reload

Open: http://localhost:5000


---

### block 3/7 — default accounts & structure
```markdown
## Default Accounts (Seeded)

**Admin**
- Username: `admin`
- Password: `admin123`

**Voters**
- `john_doe` / `password123`
- `jane_smith` / `password123`
- `mike_wilson` / `password123`
- `sarah_jones` / `password123`
- `demo_voter` / `demo123`

> Seeding is **idempotent** (reruns safely). Edit `app/seed.py` to change these.

## Project Structure
├─ app/
│ ├─ init.py # app factory (loads .env, config, registers blueprint)
│ ├─ extensions.py # db, migrate instances
│ ├─ models.py # SQLAlchemy ORM models (schema source of truth)
│ ├─ routes.py # Flask Blueprint ('main.*' endpoints)
│ ├─ seed.py # idempotent data seeding (admin/users/candidates)
│ └─ templates/
│ ├─ base.html
│ ├─ index.html
│ ├─ login.html
│ ├─ register.html
│ ├─ dashboard.html
│ ├─ results.html
│ └─ admin.html
├─ migrations/ # Alembic migration history
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example # sample env (no secrets)
└─ .gitignore
## Compose Overview

`docker-compose.yml` defines three services:

- **db** – PostgreSQL with a **named volume** (`postgres_data`) so data persists.  
- **migrate** – One-off job that runs `flask db upgrade` and seeds data, then exits.  
- **web** – Flask dev server with hot-reload (`--reload`); bind-mounts your code so edits are live.

`web` and `migrate` load common vars from `.env` and only override the DB host to `db`:
```yaml
environment:
  DATABASE_URL: postgresql://voting_user:voting_password@db:5432/voting_db
### View routes
```bash
docker compose run --rm web flask routes
Flask shell
bash
Copy code
docker compose run --rm web flask shell
Generate/apply migrations (after editing models.py)
bash
Copy code
docker compose run --rm web flask db migrate -m "your change"
docker compose run --rm web flask db upgrade
Re-seed data (idempotent)
bash
Copy code
docker compose run --rm web python - << 'PY'
from app import create_app
from app.seed import seed
app = create_app()
with app.app_context():
    seed()
    print("Seed complete")
PY
DB backups (examples)
bash
Copy code
# Dump
docker exec -t <db_container_name> \
  pg_dump -U voting_user -d voting_db > backup.sql

# Restore
type backup.sql | docker exec -i <db_container_name> \
  psql -U voting_user -d voting_db
Find the container name:

bash
Copy code
docker compose ps
go
Copy code

---

### block 6/7 — endpoints & security
```markdown
## Endpoints (client-facing URLs)

| URL                     | Method   | Purpose                           |
|------------------------|----------|-----------------------------------|
| `/`                    | GET      | Home (candidates)                 |
| `/login`               | GET/POST | Login                             |
| `/register`            | GET/POST | Register                          |
| `/dashboard`           | GET      | Voting dashboard (auth required)  |
| `/vote/<candidate_id>` | POST     | Cast a vote                       |
| `/results`             | GET      | Results                           |
| `/admin`               | GET      | Admin dashboard (admin)           |
| `/admin/add_candidate` | POST     | Add a candidate (admin)           |
| `/logout`              | GET      | Logout                            |

> Internally endpoints are namespaced (e.g., `main.login`). Use `url_for('main.<endpoint>')` in templates and redirects.

## Security Notes
- Passwords are **bcrypt-hashed**.  
- Use a strong `SECRET_KEY` in production.  
- For production, prefer Gunicorn and disable debug:
```bash
pip install gunicorn
# Example CMD in Dockerfile for prod:
# CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:create_app()"]
yaml
Copy code

---

### block 7/7 — troubleshooting, contributing, license
```markdown
## Troubleshooting

- **`env file ... .env not found`**  
  Create `.env` at the repo root (see Quick Start step 2).

- **`relation "candidate" does not exist`**  
  Migrations haven’t run yet:
  ```bash
  docker compose run --rm migrate
BuildError: Did you mean 'main.<endpoint>'?
Update templates/redirects to use url_for('main.<endpoint>') (routes live on the main blueprint).

No hot-reload
Ensure the web service bind-mounts ./:/app and starts with flask run --reload.

Contributing
Fork the repo

Create a feature branch

Make changes (tests if possible)

Open a PR

License
MIT

bash
Copy code

done ✅
::contentReference[oaicite:0]{index=0}
