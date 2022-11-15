import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from microblog.database import get_database


blueprint = Blueprint('authentication', __name__, url_prefix='/authentication')


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if not username:
            error = 'The username field is mandatory.'
        elif not password:
            error = 'The password field is mandatory.'

        if error is None:
            database = get_database()

            try:
                database.execute("""
                    INSERT INTO user (username, password)
                    VALUES (?, ?)
                """, (username, generate_password_hash(password)))
                database.commit()
            except database.IntegrityError:
                error = f'User {username} is taken earlier on.'
            else:
                return redirect(url_for('authentication.login'))
        else:
            flash(error)

    return render_template('authentication/register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        database = get_database()
        user = database.execute("""
            SELECT *
            FROM user
            WHERE username = ?
        """, (username,)).fetchone()

        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('microblog.index'))
        else:
            flash(error)

    return render_template('authentication/login.html')


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        database = get_database()
        g.user = database.execute("""
            SELECT *
            FROM user
            WHERE id = ?
        """, (user_id,)).fetchone()


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('microblog.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('authentication.login'))

        return view(**kwargs)

    return wrapped_view
