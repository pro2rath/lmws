# lwms/routes/complaint.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import get_db

complaint_bp = Blueprint('complaint', __name__)

@complaint_bp.route('/complain/<int:worker_id>', methods=['GET', 'POST'])
def submit_complaint(worker_id):
    db, cursor = get_db()
    cursor.execute('SELECT id, name FROM workers WHERE id = %s', (worker_id,))
    worker = cursor.fetchone()

    if not worker:
        flash('Worker not found.', 'danger')
        return redirect(url_for('search.search'))

    if request.method == 'POST':
        reason = request.form['reason']
        if not reason:
            flash('Please provide a reason for the complaint.', 'danger')
        else:
            cursor.execute('INSERT INTO complaints (worker_id, reason) VALUES (%s, %s)', (worker_id, reason))
            db.commit()
            flash('Complaint submitted successfully. An admin will review it.', 'success')
            return redirect(url_for('search.search'))

    return render_template('complaint.html', worker=worker)