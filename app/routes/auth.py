from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    g,
)

from app.crud.crud_user import crud_user
from app.db import get_db
from app.utils import check_form_data

auth_bp = Blueprint("auth", __name__)


@auth_bp.before_app_request
def load_logged_in_user():
    user_username = session.get("user_username")
    if not user_username:
        g.user = None
    else:
        db = get_db()
        g.user = crud_user.read(db, user_username)


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapper


def not_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user:
            return redirect(url_for("private.index"))
        return view(*args, **kwargs)

    return wrapper


@auth_bp.route("/register", methods=["GET", "POST"])
@auth_bp.route("/signup", methods=["GET", "POST"])
@not_required
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        err = check_form_data(username=username, email=email, password=password)
        if not err:
            db = get_db()
            err = crud_user.create(db, username, email, password)
            if not err:
                return redirect(url_for("auth.login"))
        flash(err)
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@not_required
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        err = check_form_data(username=username, password=password)
        if not err:
            db = get_db()
            err = crud_user.authenticate(db, username, password)
            if not err:
                session.clear()
                session["user_username"] = username
                return redirect(url_for("private.index"))
        flash(err)
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
