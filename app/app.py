import os
from secrets import token_urlsafe

from flask import Flask

from app import db
from app.routes.auth import auth_bp
from app.routes.private import private_bp


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=token_urlsafe(64),
        DB=os.getenv("FLASK_DATABASE"),
        DB_HOST=os.getenv("FLASK_DATABASE_HOST"),
        DB_USER=os.getenv("FLASK_DATABASE_USER"),
        DB_PASSWORD=os.getenv("FLASK_DATABASE_PASSWORD"),
    )
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(private_bp)
    return app
