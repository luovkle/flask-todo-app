import logging

from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from app.crud.crud_task import crud_task
from app.db import get_db
from app.routes.auth import login_required
from app.utils import check_form_data

logger = logging.getLogger(__name__)

private_bp = Blueprint("private", __name__)


@private_bp.route("/", methods=["GET"])
@login_required
def index():
    logger.info(f"{request.remote_addr} {request.method} {request.path}")
    user = g.get("user")
    db = get_db()
    tasks = crud_task.read(db, user["id"])
    return render_template("private/index.html", tasks=tasks)


@private_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        logger.info(f"{request.remote_addr} {request.method} {request.path}")
        title = request.form.get("title")
        description = request.form.get("description")
        err = check_form_data(title=title, description=description)
        if not err:
            db = get_db()
            err = crud_task.create(db, g.user["id"], title, description)
            if not err:
                return redirect(url_for("private.index"))
        flash(err)
    logger.info(f"{request.remote_addr} {request.method} {request.path}")
    return render_template("private/create.html")


@private_bp.route("/<string:task_title>/update", methods=["GET", "POST"])
@login_required
def update(task_title):
    if request.method == "POST":
        logger.info(f"{request.remote_addr} {request.method} {request.path}")
        new_title = request.form.get("new_title")
        new_description = request.form.get("new_description")
        err = check_form_data(
            current_title=task_title,
            new_title=new_title,
            new_description=new_description,
        )
        if not err:
            db = get_db()
            err = crud_task.update(
                db, g.user["id"], task_title, new_title, new_description
            )
            if not err:
                return redirect(url_for("private.index"))
        flash(err)
    logger.info(f"{request.remote_addr} {request.method} {request.path}")
    db = get_db()
    task = crud_task.read(db, g.user["id"], task_title)
    if not task:
        abort(404)
    return render_template(
        "private/update.html", title=task["title"], description=task["description"]
    )


@private_bp.route("/<string:task_title>/delete", methods=["GET", "POST"])
@login_required
def delete(task_title):
    if request.method == "POST":
        logger.info(f"{request.remote_addr} {request.method} {request.path}")
        db = get_db()
        err = crud_task.delete(db, g.user["id"], task_title)
        if not err:
            return redirect(url_for("private.index"))
        flash(err)
    logger.info(f"{request.remote_addr} {request.method} {request.path}")
    db = get_db()
    task = crud_task.read(db, g.user["id"], task_title)
    if not task:
        abort(404)
    return render_template("private/delete.html")
