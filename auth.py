from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('auth.register'))
        if User.find_by_username(username):
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        try:
            user = User(username)
            user.password_hash = user.generate_password_hash(password)  # Wait, fix: Use generate_password_hash directly
            user.save()
            login_user(user)
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            print(f"Registration error: {e}")  # Logs to Render console
            flash('Registration failed. Check logs.')
            return redirect(url_for('auth.register'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
