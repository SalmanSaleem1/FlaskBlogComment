from flaskface import db, bcrypt, _
from flask import render_template, redirect, request, flash, url_for, Blueprint, jsonify, abort
from flaskface.user.Forms import RegisterForm, LoginForm, AccountForm, RequestResetForm, RequestPasswordForm, \
    MessageForm
from flaskface.Models import User, UserSchema, Post, Message
from flask_login import login_user, current_user, logout_user, login_required
from marshmallow import pprint
from flaskface.user.Utils import save_picture, send_reset_email
from flaskface.constant.app_constant import constants

user = Blueprint('user', __name__)


@user.route('/registers', methods=['POST', 'GET'])
def registers():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=form.password.data)
        # user = User(name=form.name.data, username=form.name.data, email=form.email.data,
        #             password=hashed_password)
        sechma = UserSchema()
        result = sechma.dump(user)
        pprint(result.data)
        db.session.add(user)
        db.session.commit()
        flash(_(f'{constants.REGISTER_SUCCESS}'), 'success')
        return redirect(url_for('user.login'))

    return render_template('Register.html', title='Register', form=form)


@user.route('/login', methods=['POST', 'GET'])
def login():
    # api_key = request.headers.get('api_key')
    #
    # if api_key is None:
    #     abort(403, 'Empty api key')
    #
    # if api_key != '123456':
    #     abort(403, 'Wrong Api key')
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            schema = UserSchema()
            result = schema.dump(user)
            pprint(result.data)
            flash(_(f'{constants.LOGIN_SUCCESS}'), 'success')
            return redirect(url_for('main.home'))
        else:
            flash(constants.INVALID_EMAIL_PASSWORD, 'danger')
    return render_template('LoginForm.html', form=form, title='Login')


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user.route('/user/<string:username>', methods=['POST', 'GET'])
@login_required
def account(username):
    print('salman here')
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('Account.html', user=user, title=user.username)


@user.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('UserPopUp.html', user=user)


@user.route('/account', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = AccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('Edit_Profile.html', title='Account', form=form, image_file=image_file)


@user.route('/follow/<string:username>', methods=['POST', 'GET'])
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_(f"User {user} not found"), 'info')

        return redirect(url_for('index'))
    if user == current_user:
        flash(_(f"{constants.YOU_CAN_NOT_FOLLOW_YOURSELF}"), "warning")
        return redirect(url_for('account', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_(f'{constants.YOU_ARE_FOLLOWING} {username}'), "success")
    return redirect(url_for('user.account', username=username))


@user.route('/unfollow/<username>', methods=['POST', 'GET'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('index'))
    if user == current_user:
        flash(_(f'{constants.YOU_CAN_NOT_FOLLOW_YOURSELF}'), 'warning')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_(f'You are unfollowing {username}'), 'warning')
    return redirect(url_for('user.account', username=username))


@user.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.create_at.desc()).paginate(page=page, per_page=5,
                                                                                       error_out=False)
    return render_template('UserPosts.html', posts=posts, user=user)


@user.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
    return render_template('RequestReset.html', title='Reset Request', form=form)


@user.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(constants.INVALID_TOKEN, 'warning')
        return redirect(url_for('user.reset_request'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash(constants.UPDATE_PASSWORD, 'success')
        return redirect(url_for('user.login'))
    return render_template('ResetPassword.html', title='Reset Password', form=form)


@user.route('/photos/<int:user_id>', methods=['POST', 'GET'])
def photos(user_id):
    user_pics = Post.query.filter_by(user_id=current_user.id)
    return render_template('Photos.html', user_pics=user_pics)


@user.route('/send_message/<recipient>', methods=['POST', 'GET'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():

        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_(f'{constants.MESSAGE_SEND}'), 'info')
        return redirect(url_for('user.account', username=recipient))

    return render_template('Send_Message.html', title=_('Send Message'),
                           form=form, recipient=recipient)
