from flask import render_template, url_for, flash, redirect, Blueprint
from maintenance_system import db, bycrypt, app
from maintenance_system.models import User
from .forms import UserForm, LoginForm, UpdateUserForm
from flask_login import login_user, current_user, logout_user, login_required
import os
from PIL import Image


usersbp = Blueprint('usersbp', __name__)


@usersbp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = bycrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('User has been created successfully!', 'success')
        return redirect(url_for('usersbp.login'))
    return render_template('register.html', form=form)


@usersbp.route('/login', methods=['GET', 'POST'])
def login():
    """Login a user"""
    if current_user.is_authenticated:
        return redirect(url_for('usersbp.users', id=current_user.id))
    form = LoginForm()
    form.submit.label.text = 'Login'
    print(form.errors)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bycrypt.check_password_hash(user.password, form.password.data):
            flash(f'Hello {user.username}. You are logged in succsessfully!', 'success')
            login_user(user)
            if current_user.rank == 'Admin':
                return redirect(url_for('usersbp.users'))
            return redirect(url_for('usersbp.user', id=current_user.id))
        else:
            flash('Login Unsuccessfull! Please check username and password', 'danger')
    return render_template('login.html', form=form)

@login_required
@usersbp.route('/logout')
def logout():
    """Logout a user"""
    logout_user()
    flash('You are logged out successfully!', 'success')
    return redirect(url_for('main.home'))

@login_required
@usersbp.route('/users')
def users():
    """Get all users"""
    if not current_user.is_authenticated:
        return redirect(url_for('usersbp.login'))
    users = User.query.all()
    return render_template('users.html', users=users)

@login_required
@usersbp.route('/users/<int:id>')
def user(id):
    """Get a user by id"""
    if not current_user.is_authenticated:
        return redirect(url_for('usersbp.login'))
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

@login_required
@usersbp.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    """Update a user by id"""
    if not current_user.is_authenticated:
        return redirect(url_for('usersbp.login'))
    user = User.query.get_or_404(id)
    form = UpdateUserForm()
    form.username.data = user.username
    form.email.data = user.email
    print(os.path.abspath(__file__))
    if form.validate_on_submit():
        if form.picture.data:
            _, file_ext = os.path.splitext(form.picture.data.filename)
            picture_file = f'{form.username.data}{file_ext}'
            output_size = (500, 500)
            i = Image.open(form.picture.data)
            i.thumbnail(output_size)
            i.save(os.path.join(app.root_path, 'static/images/', picture_file))
            # form.picture.data.save(os.path.join(app.root_path, 'static/images/', picture_file))
            user.profile_pic = picture_file
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('User has been updated successfully!', 'success')
        return redirect(url_for('usersbp.user', id=user.id))
    return render_template('update_user.html', form=form)
