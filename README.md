# Voting Platform

A simple Flask web application for voting, built with **Flask + SQLAlchemy**, using **PostgreSQL** by default and containerized with **Docker Compose**. It includes user accounts, candidate management, and live results.

---

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

---

## Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy  
- **DB**: PostgreSQL (Docker)  
- **Migrations**: Alembic via Flask-Migrate  
- **Frontend**: Jinja2 templates, Bootstrap 5  
- **Containers**: Docker + Docker Compose  

---

## Quick Start (Docker – Recommended)

### 1) Clone and enter the project folder
```bash
git clone https://github.com/RMITSSD/ssd-assignment3-voter-registration.git
cd ssd-assignment3-voter-registration
