
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import db
from ..models import User, ROLE_SUPERADMIN, ROLE_ADMIN, ROLE_USER
from ..forms import LoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data.lower()).first()
        if u and check_password_hash(u.password_hash, form.password.data):
            login_user(u)
            flash("Welcome back!", "success"); return redirect(url_for("assets.dashboard"))
        flash("Invalid credentials", "error")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/users", methods=["GET","POST"])
@login_required
def users():
    if current_user.role != ROLE_SUPERADMIN:
        flash("Superadmin only", "error")
        return redirect(url_for("assets.dashboard"))
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        role = request.form.get("role", ROLE_USER)
        pw = request.form.get("password","")
        if not (name and email and pw):
            flash("All fields are required", "error")
        elif User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
        else:
            u = User(name=name, email=email, role=role, password_hash=generate_password_hash(pw))
            db.session.add(u); db.session.commit()
            flash("User added", "success")
            return redirect(url_for("auth.users"))
    users = User.query.order_by(User.id.desc()).all()
    return render_template("auth/users.html", users=users, roles=[ROLE_SUPERADMIN, ROLE_ADMIN, ROLE_USER])
