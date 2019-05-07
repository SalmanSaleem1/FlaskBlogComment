from flask import Blueprint, render_template, redirect, url_for, abort, flash, request
from flaskface.post.Forms import NewPostForm, AddCommentForm
from flaskface.Models import Post, PostSchema, Comment
from flaskface import db, pusher_client
from flask_login import current_user, login_required
from marshmallow import pprint
from flaskface.constant.app_constant import Constants

post = Blueprint('post', __name__)


@post.route('/newpost', methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        sechma = PostSchema()
        result = sechma.dump(post)
        pprint(result.data)
        flash(f'{Constants.POST_SUCCESS}', 'success')
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
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'{Constants.UPDATE_SUCCESS}', 'success')
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
    flash(f'{Constants.DELETE_SUCCESS}', 'success')
    return redirect(url_for('main.home'))


@post.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comm = Comment.query.filter_by(post_id=post.id)
    form = AddCommentForm()
    if form.validate_on_submit() or request.method == 'POST':
        print('salman test comment')
        myComment = request.form['myComment']
        # myComment = form.body.data
        post_by_id = post_id
        user_by_id = current_user.username
        comment = Comment(body=myComment, post_id=post_by_id, user_id=user_by_id)
        db.session.add(comment)
        db.session.commit()

        flash("Your comment has been added to the post", "success")
        data = {

            "myComment": myComment,

        }
        pusher_client.trigger('Blog', 'new_comment', {'data': print(data)})
        return redirect(url_for("post.post_detail", post_id=post.id))
    return render_template("Post.html", title="Comment Post", form=form, post=post, post_id=post_id, comm=comm)


@post.route("/comment/<int:com_id>", methods=["GET", "POST"])
@login_required
def delete_comment(com_id):
    # post = Post.query.get_or_404(com_id)
    comm = Comment.query.get_or_404(com_id)

    if comm.user_id != current_user:
        abort(404)
    db.session.delete(comm)
    db.session.commit()
    # pprint({'Delete Success': result.data})
    flash(f'{Constants.DELETE_SUCCESS}', 'success')
    return redirect(url_for("main.home"))
