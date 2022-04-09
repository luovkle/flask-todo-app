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
def init_db_command():
    db = get_db()
    with db.cursor() as cur:
        sql = """
        SELECT EXISTS (
            SELECT FROM
                pg_tables
            WHERE
                schemaname = 'public' AND
                tablename = 'users'
        );
        """
        cur.execute(sql)
        resp = cur.fetchone()
        if resp[0] is True:
            click.echo("The database is already initialized")
        else:
            with current_app.open_resource("schema.sql") as f:
                sql = f.read().decode()
            cur.execute(sql)
            db.commit()
            click.echo("The database has been initialized")


@click.command("reset-db")
@with_appcontext
def reset_db_command():
    db = get_db()
    with db.cursor() as cur:
        with current_app.open_resource("schema.sql") as f:
            sql = f.read().decode()
        cur.execute(sql)
    db.commit()
    click.echo("The database has been reset")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_db_command)
