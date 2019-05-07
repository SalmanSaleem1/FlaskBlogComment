from flask import Blueprint, render_template

comment = Blueprint('comment', __name__)


@comment.route('/index')
def index():
    return render_template('index.html')
