from flask import render_template, url_for, flash, redirect, Blueprint
from maintenance_system import db, bycrypt
from maintenance_system.models import User
from maintenance_system.forms import UserForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


usersbp = Blueprint('usersbp', __name__)


@usersbp.route('/register', methods=['GET', 'POST'])
def register():
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    form.submit.label.text = 'Login'
    print(form.errors)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bycrypt.check_password_hash(user.password, form.password.data):
            flash(f'Hello {user.username}. You are logged in succsessfully!', 'success')
            login_user(user)
            return redirect(url_for('usersbp.user',id=current_user.id))
        else:
            flash('Login Unsuccessfull! Please check username and password', 'danger')
    return render_template('login.html', form=form)
@usersbp.route('/logout')
def logout():
    logout_user()
    flash('You are logged out successfully!', 'success')
    return redirect(url_for('home'))

@usersbp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@usersbp.route('/users/<int:id>')
def user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)
