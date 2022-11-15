from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort

from microblog.authentication import login_required
from microblog.database import get_database


blueprint = Blueprint('microblog', __name__)


@blueprint.route('/')
def index():
    database = get_database()
    posts = database.execute("""
        SELECT post.id,
               title,
               body,
               date_created,
               author_id,
               username
        FROM post
        JOIN user
        ON post.author_id = user.id
        ORDER BY date_created
        DESC
    """).fetchall()

    return render_template('microblog/index.html', posts=posts)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'The title is mandatory.'

        if error is not None:
            flash(error)
        else:
            database = get_database()
            database.execute("""
                INSERT INTO post (title, body, author_id)
                VALUES (?, ?, ?)
            """, (title, body, g.user['id']))
            database.commit()

            return redirect(url_for('microblog.index'))

    return render_template('microblog/create.html')


def get_post(id, check_author=True):
    database = get_database()
    post = database.execute("""
        SELECT post.id,
               title,
               body,
               date_created,
               author_id,
               username
        FROM post
        JOIN user
        ON post.author_id = user.id
        WHERE post.id = ?
    """, (id,)).fetchone()

    if post is None:
        abort(404, f'Post {id} does not exist.')

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'The title is mandatory.'

        if error is not None:
            flash(error)
        else:
            database = get_database()
            database.execute("""
                UPDATE post
                SET title = ?,
                    body = ?
                WHERE id = ?
            """, (title, body, id))
            database.commit()

            return redirect(url_for('microblog.index'))

    return render_template('microblog/update.html', post=post)


@blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)

    database = get_database()
    database.execute("""
        DELETE
        FROM post
        WHERE id = ?
    """, (id,))
    database.commit()

    return redirect(url_for('microblog.index'))
