from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Mantra

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    mantras = Mantra.get_all_by_user(current_user.id)
    return render_template('dashboard.html', mantras=mantras)

@main.route('/add_mantra', methods=['GET', 'POST'])
@login_required
def add_mantra():
    if request.method == 'POST':
        name = request.form['name']
        syllables = int(request.form['syllables'])
        mantra = Mantra(name=name, syllables=syllables, user_id=current_user.id)
        mantra.save()
        flash('Mantra added successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_mantra.html')

@main.route('/add_entry/<int:mantra_id>', methods=['POST'])
@login_required
def add_entry(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if mantra and mantra.user_id == current_user.id:
        date = request.form['date']
        count = int(request.form['count'])
        mantra.add_entry(date, count)
        flash('Entry added successfully!')
    return redirect(url_for('main.mantra_detail', mantra_id=mantra_id))

@main.route('/mantra_records')
@login_required
def mantra_records():
    mantras = Mantra.get_all_by_user(current_user.id)
    return render_template('mantra_list.html', mantras=mantras)

@main.route('/mantra_detail/<int:mantra_id>')
@login_required
def mantra_detail(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if not mantra or mantra.user_id != current_user.id:
        flash('Access denied!')
        return redirect(url_for('main.mantra_records'))
    return render_template('mantra_detail.html', mantra=mantra)

@main.route('/edit_mantra/<int:mantra_id>', methods=['POST'])
@login_required
def edit_mantra(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if mantra and mantra.user_id == current_user.id:
        name = request.form['name']
        syllables = int(request.form['syllables'])
        mantra.update(name, syllables)
        flash('Mantra updated successfully!')
    return redirect(url_for('main.mantra_detail', mantra_id=mantra_id))

@main.route('/delete_mantra/<int:mantra_id>')
@login_required
def delete_mantra(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if mantra and mantra.user_id == current_user.id:
        Mantra.delete(mantra_id)
        flash('Mantra deleted successfully!')
    return redirect(url_for('main.mantra_records'))

@main.route('/delete_entry/<int:entry_id>')
@login_required
def delete_entry(entry_id):
    Mantra.delete_entry(entry_id)
    flash('Entry deleted successfully!')
    return redirect(request.referrer or url_for('main.mantra_records'))
