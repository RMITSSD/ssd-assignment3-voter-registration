# app/seed.py
from .extensions import db
from .models import User, Candidate
import bcrypt

def seed():
    # admin
    if not User.query.filter_by(username="admin").first():
        pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
        db.session.add(User(username="admin", password=pw, is_admin=True))

    # voters
    for u, p in [
        ("john_doe", "password123"),
        ("jane_smith", "password123"),
        ("mike_wilson", "password123"),
        ("sarah_jones", "password123"),
        ("demo_voter", "demo123"),
    ]:
        if not User.query.filter_by(username=u).first():
            pw = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
            db.session.add(User(username=u, password=pw))

    if not Candidate.query.count():
        db.session.add_all([
            Candidate(name="Alice Johnson", party="Progressive Party", description="Education & healthcare."),
            Candidate(name="Bob Smith", party="Conservative Alliance", description="Economic growth."),
            Candidate(name="Carol Davis", party="Green Movement", description="Sustainability."),
        ])

    db.session.commit()
