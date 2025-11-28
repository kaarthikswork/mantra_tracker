from flask import Blueprint, render_template, request, redirect, url_for, session, flash

main = Blueprint('main', __name__)

# Helper to get mantras from session
def get_mantras():
    return session.get('mantras', [])

# Helper to save mantras to session
def save_mantras(mantras):
    session['mantras'] = mantras

# Helper to calculate current status (sum of all chanting counts)
def get_current_status():
    mantras = get_mantras()
    total = 0
    for mantra in mantras:
        for entry in mantra.get('entries', []):
            total += entry['count']
    return total

@main.route('/')
def dashboard():
    mantras = get_mantras()
    current_status = get_current_status()
    return render_template('dashboard.html', mantras=mantras, current_status=current_status)

@main.route('/add_mantra', methods=['GET', 'POST'])
def add_mantra():
    if request.method == 'POST':
        name = request.form['name']
        syllables = int(request.form['syllables'])
        purascharana_count = syllables * 100000
        mantras = get_mantras()
        mantras.append({
            'id': len(mantras) + 1,  # Simple incremental ID
            'name': name,
            'syllables': syllables,
            'purascharana_count': purascharana_count,
            'entries': []  # List of {date, count}
        })
        save_mantras(mantras)
        flash('Mantra added successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_mantra.html')

@main.route('/add_entry/<int:mantra_id>', methods=['POST'])
def add_entry(mantra_id):
    mantras = get_mantras()
    mantra = next((m for m in mantras if m['id'] == mantra_id), None)
    if mantra:
        date = request.form['date']
        count = int(request.form['count'])
        mantra['entries'].append({'date': date, 'count': count})
        save_mantras(mantras)
        flash('Entry added successfully!')
    return redirect(url_for('main.dashboard'))
