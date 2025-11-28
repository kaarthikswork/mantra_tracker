from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Mantra, get_current_status

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    mantras = Mantra.get_all()
    return render_template('dashboard.html', mantras=mantras)

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
    return redirect(url_for('main.mantra_detail', mantra_id=mantra_id))

@main.route('/mantra_records')
def mantra_records():
    mantras = Mantra.get_all()
    return render_template('mantra_list.html', mantras=mantras)

@main.route('/mantra_detail/<int:mantra_id>')
def mantra_detail(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if not mantra:
        flash('Mantra not found!')
        return redirect(url_for('main.mantra_records'))
    return render_template('mantra_detail.html', mantra=mantra)

@main.route('/edit_mantra/<int:mantra_id>', methods=['POST'])
def edit_mantra(mantra_id):
    mantra = Mantra.get_by_id(mantra_id)
    if mantra:
        name = request.form['name']
        syllables = int(request.form['syllables'])
        mantra.update(name, syllables)
        flash('Mantra updated successfully!')
    return redirect(url_for('main.mantra_detail', mantra_id=mantra_id))

@main.route('/delete_mantra/<int:mantra_id>')
def delete_mantra(mantra_id):
    Mantra.delete(mantra_id)
    flash('Mantra deleted successfully!')
    return redirect(url_for('main.mantra_records'))

@main.route('/delete_entry/<int:entry_id>')
def delete_entry(entry_id):
    Mantra.delete_entry(entry_id)
    flash('Entry deleted successfully!')
    return redirect(request.referrer or url_for('main.mantra_records'))
