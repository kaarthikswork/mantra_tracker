from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Mantra
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    mantras = Mantra.find_by_user(current_user.username)
    return render_template('dashboard.html', mantras=mantras)

@main.route('/add_mantra', methods=['GET', 'POST'])
@login_required
def add_mantra():
    if request.method == 'POST':
        name = request.form['name']
        syllables = int(request.form['syllables'])
        mantra = Mantra(current_user.username, name, syllables)
        mantra.save()
        return redirect(url_for('main.dashboard'))
    return render_template('add_mantra.html')

@main.route('/add_entry/<mantra_id>', methods=['POST'])
@login_required
def add_entry(mantra_id):
    mantra = Mantra.find_by_id(mantra_id)
    if mantra and mantra['user_id'] == current_user.username:
        date = request.form['date']
        count = int(request.form['count'])
        mantra_obj = Mantra(mantra['user_id'], mantra['name'], mantra['syllables'])
        mantra_obj._id = mantra['_id']
        mantra_obj.add_entry(date, count)
    return redirect(url_for('main.dashboard'))
