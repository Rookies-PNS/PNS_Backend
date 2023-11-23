from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from bod import db
from bod.models import Post, Comment

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:post_id>', methods=('POST',))
def create(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    comment = Comment(content=content, create_date=datetime.now())
    post.comment_set.append(comment)
    db.session.commit()
    return redirect(url_for('post.detail', post_id=post_id))
