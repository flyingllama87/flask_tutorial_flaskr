from flask import (
    Blueprint, flash, g, redirect, url_for, request, render_template
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__,)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DISC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)