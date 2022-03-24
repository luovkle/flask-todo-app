import click
import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            database=current_app.config["DB"],
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


@click.command("init-db")
@with_appcontext
def init_app_command():
    db = get_db()
    with db.cursor() as cur:
        with current_app.open_resource("schema.sql") as f:
            sql = f.read().decode()
        cur.execute(sql)
    db.commit()
    click.echo("Init database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_app_command)
