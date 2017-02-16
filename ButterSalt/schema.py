import sqlite3
from flask import g
from ButterSalt import app


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(app.config['SQL'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def show_entries(table):
    with app.app_context():
        db = get_db()
        cur = db.execute('select * from %s order by id desc' % table)
        entries = [[r for r in row] for row in cur.fetchall()]
        return entries


def add_modules_history(tgt, fun, args, kwargs, user_id='None'):
    with app.app_context():
        db = get_db()
        db.execute('insert into moudle_execute_history '
                   '(tgt, fun, args, kwargs, user_id) '
                   'values (?, ?, ?, ?, ?)',
                   [tgt, fun, args, kwargs, user_id])
        db.commit()
