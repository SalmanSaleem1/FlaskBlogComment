from flask import Blueprint, render_template, request
from flask_login import login_required
from flaskface.Models import Post
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.create_at.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = current_user.followed_posts().all()
    return render_template('Home.html', title='Home', posts=posts)
