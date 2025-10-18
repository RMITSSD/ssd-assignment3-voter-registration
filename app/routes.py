from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .extensions import db
from .models import User, Candidate, Vote
from sqlalchemy import func
import bcrypt

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    candidates = Candidate.query.all()
    return render_template("index.html", candidates=candidates)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = user.is_admin
            return redirect(url_for("main.dashboard"))
        flash("Invalid username or password")
    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return render_template("register.html")
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(username=username, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for("main.login"))
    return render_template("register.html")

@bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    user = User.query.get(session["user_id"])
    candidates = Candidate.query.all()
    return render_template("dashboard.html", user=user, candidates=candidates)

@bp.route("/vote/<int:candidate_id>", methods=["POST"])
def vote(candidate_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    user = User.query.get(session["user_id"])
    if user.has_voted:
        flash("You have already voted!")
        return redirect(url_for("main.dashboard"))

    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        flash("Candidate not found!")
        return redirect(url_for("main.dashboard"))

    db.session.add(Vote(user_id=user.id, candidate_id=candidate.id))
    candidate.votes_count = (candidate.votes_count or 0) + 1
    user.has_voted = True
    db.session.commit()
    flash(f"Your vote for {candidate.name} has been recorded!")
    return redirect(url_for("main.results"))

@bp.route("/results")
def results():
    # order by votes desc; safe when None
    candidates = Candidate.query.order_by(Candidate.votes_count.desc()).all()
    total_votes = db.session.query(func.coalesce(func.sum(Candidate.votes_count), 0)).scalar()
    return render_template("results.html", candidates=candidates, total_votes=total_votes)

@bp.route("/admin")
def admin():
    if "user_id" not in session or not session.get("is_admin"):
        flash("Admin access required!")
        return redirect(url_for("main.login"))
    candidates = Candidate.query.all()
    users = User.query.all()
    return render_template("admin.html", candidates=candidates, users=users)

@bp.route("/admin/add_candidate", methods=["POST"])
def add_candidate():
    if "user_id" not in session or not session.get("is_admin"):
        return redirect(url_for("main.login"))
    name = request.form["name"].strip()
    party = request.form.get("party", "").strip()
    description = request.form.get("description", "").strip()
    db.session.add(Candidate(name=name, party=party, description=description))
    db.session.commit()
    flash(f"Candidate {name} added successfully!")
    return redirect(url_for("main.admin"))

@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))
