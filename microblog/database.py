import sqlite3

import click
from flask import current_app, g


def get_database():
    if 'database' not in g:
        g.database = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row

    return g.database


def close_database(synthetic_event=None):
    database = g.pop('database', None)

    if database is not None:
        database.close()


def initialize_database():
    database = get_database()

    with current_app.open_resource('schema.sql') as file:
        database.executescript(file.read().decode('utf8'))


@click.command('initialize-database')
def initialize_database_command():
    initialize_database()
    click.echo('Initialized')


def initialize_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(initialize_database_command)
