from datetime import datetime

from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from flask_login import login_required

from flaskface import app, db
from flaskface.Models import Post, Message, Notifications

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.create_at.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    # posts = current_user.followed_posts().all()
    return render_template('Home.html', title='Home', posts=posts)


@main.route('/message', methods=['POST', 'GET'])
@login_required
def message():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    return render_template('Messages.html', messages=messages)


@main.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notifications.timestamp > since).order_by(Notifications.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@main.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.create_at.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    return render_template('Home.html', title='Explore', posts=posts)
