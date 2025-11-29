from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required  # Added login_required
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = User.register(email, password)
            login_user(user)
            flash('Registration successful!')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}')
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = User.login(email, password)
            if user:
                login_user(user)
                return redirect(url_for('main.dashboard'))
            flash('Invalid credentials')
        except Exception as e:
            flash(f'Login failed: {str(e)}')
    return render_template('login.html')

@auth.route('/logout')
@login_required  # This was missing the import
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
