from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Mantra, get_current_status

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    mantras = Mantra.get_all()
    current_status = get_current_status()
    return render_template('dashboard.html', mantras=mantras, current_status=current_status)

@main.route('/add_mantra', methods=['GET', 'POST'])
def add_mantra():
    if request.method == 'POST':
        name = request.form['name']
        syllables = int(request.form['syllables'])
        mantra = Mantra(name=name, syllables=syllables)
        mantra.save()
        flash('Mantra added successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_mantra.html')

@main.route('/add_entry/<int:mantra_id>', methods=['POST'])
def add_entry(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if mantra:
        date = request.form['date']
        count = int(request.form['count'])
        mantra.add_entry(date, count)
        flash('Entry added successfully!')
    return redirect(url_for('main.dashboard'))

@main.route('/mantra_records')
def mantra_records():
    mantras = Mantra.get_all()
    return render_template('mantra_list.html', mantras=mantras)

@main.route('/mantra_entries/<int:mantra_id>')
def mantra_entries(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if not mantra:
        flash('Mantra not found!')
        return redirect(url_for('main.mantra_records'))
    return render_template('mantra_entries.html', mantra=mantra)
