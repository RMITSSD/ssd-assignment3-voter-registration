from datetime import datetime
from .extensions import db

class User(db.Model):
    __tablename__ = "user"
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    password   = db.Column(db.String(128), nullable=False)  # store a hash!
    has_voted  = db.Column(db.Boolean, default=False)
    is_admin   = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    votes = db.relationship("Vote", backref="user", lazy=True)

class Candidate(db.Model):
    __tablename__ = "candidate"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    party       = db.Column(db.String(100))
    description = db.Column(db.Text)
    votes_count = db.Column(db.Integer, default=0)  # renamed from 'votes' to be clearer
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    votes = db.relationship("Vote", backref="candidate", lazy=True)

class Vote(db.Model):
    __tablename__ = "vote"
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"), nullable=False)
    voted_at     = db.Column(db.DateTime, default=datetime.utcnow)
