from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint(
    "auth",
    __name__,
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        firstname = request.form.get("firstName")
        lastname = request.form.get("lastName")
        password_1 = request.form.get("password1")
        password_2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists", category="error")
        elif len(email) < 4:
            flash("Email too short", category="error")
        elif len(firstname) < 1:
            flash("Name too short", category="error")
        elif len(lastname) < 1:
            flash("Last name too short", category="error")
        elif password_1 != password_2:
            flash("Passwords don't match", category="error")
        elif not validate_password(password_1):
            flash(
                "Password must be at least eight characters long, and contains one uppercase letter, one lowercase letter and one digit",
                category="error",
            )
        else:
            new_user = User(
                email,
                username,
                firstname,
                lastname,
                generate_password_hash(password_1, method="scrypt"),
            )
            db.session.add(new_user)
            flash(message="Sucess")
            db.session.commit()
            return redirect(url_for("views.home"))
    return render_template("sign_up.html")


def validate_password(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

    # Testing the password against the pattern using re.match
    match = re.match(pattern, password)

    # Return true if matched otherwise false
    return bool(match)
