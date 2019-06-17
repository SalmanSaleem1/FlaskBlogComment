from flask import Blueprint, render_template, redirect, url_for, abort, flash, request, jsonify
from flaskface.post.Forms import NewPostForm, AddCommentForm
from flaskface.Models import Post, PostSchema, Comment, User
from flaskface import db, _
from flask_login import current_user, login_required
from marshmallow import pprint
from flaskface.post.utils import save_picture
from guess_language import guess_language
from flaskface.constant.app_constant import constants
import requests

post = Blueprint('post', __name__)


@post.route('/newpost', methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        language = guess_language(form.content.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
        post = Post(title=form.title.data, content=form.content.data, image_file=picture_file,
                    author=current_user, my_language=language)
        db.session.add(post)
        db.session.commit()
        sechma = PostSchema()
        result = sechma.dump(post)
        pprint(result.data)
        flash(_(f'{constants.YOUR_POST_IS_LIVE_NOW}'), 'success')
        return redirect(url_for('main.home'))

    return render_template('NewPost.html', title='New Post', form=form, legend='New Post')


@post.route('/newpost/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    form = NewPostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()
        flash(f'{constants.UPDATE_SUCCESS}', 'success')
        return redirect(url_for('main.home'))
    form.title.data = post.title
    form.content.data = post.content

    schema = PostSchema()
    result = schema.load(post)
    pprint({'Post Id': result})
    return render_template('NewPost.html', title='Post', legend='Update Post', form=form)


@post.route('/newpost/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    schema = PostSchema()
    result = schema.dump(post)
    pprint({'Delete Success': result.data})
    flash(_(f'{constants.DELETE_SUCCESS}'), 'success')
    return redirect(url_for('main.home'))


@post.route("/post/<string:username>/<int:post_id>", methods=["GET", "POST"])
@login_required
def post_detail(username, post_id):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user) or current_user == user:
        al_posts = Post.query.filter_by(author=user).all()
        all_posts_ids = [item.id for item in al_posts]
        if post_id in all_posts_ids or current_user.is_following(user):
            post = Post.query.get_or_404(post_id)
            comm = Comment.query.filter_by(post_id=post.id)
            form = AddCommentForm()
            if form.validate_on_submit() or request.method == 'POST':
                myComment = request.form['myComment']
                # myComment = form.body.data
                post_by_id = post_id
                user_by_id = current_user.username
                comment = Comment(body=myComment, post_id=post_by_id, user_id=user_by_id)
                db.session.add(comment)
                db.session.commit()
                data = {

                    "myComment": myComment,

                }
                # pusher_client.trigger('Blog', 'new_comment', {'data': print(data)})
                return redirect(url_for("post.post_detail", post_id=post.id, username=username))
        else:
            flash(f'{constants.THE_LINK_IS_NOT_FOLLOWING_BY_YOU}', 'info')
            return redirect(url_for('main.home'))
            # return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.home'))
    return render_template("Post.html", title="Comment Post", form=form, post=post, post_id=post_id,
                           comm=comm, user=user)


@post.route("/comment/<int:com_id>", methods=["GET", "POST"])
@login_required
def delete_comment(com_id):
    post = Post.query.get_or_404(com_id)
    comm = Comment.query.get_or_404(com_id)

    if comm.user_id != current_user and comm.user_id != post.author.username:
        abort(404)
    db.session.delete(comm)
    db.session.commit()
    # pprint({'Delete Success': result.data})
    flash(_(f'{constants.DELETE_SUCCESS}'), 'success')
    return redirect(url_for("main.home"))


@post.route('/like/<int:post_id>/<action>', methods=["GET", "POST"])
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.post_like(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()

    return jsonify({"totalCounts": post.likes.count()})


@post.route('/check')
def check():
    return render_template('testAjax.html')


@post.route('/process', methods=["GET", "POST"])
def process():
    name = request.form['name']
    email = request.form['email']
    if name and email:
        new_name = name[::-1]
        return jsonify({'name': new_name})
    return jsonify({'error': 'Missing Data'})
