# lwms/routes/admin.py
import os
from functools import wraps
from flask import (Blueprint, render_template, request, flash, redirect, url_for, session, current_app)
from app import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash('You were successfully logged in', 'success')
            return redirect(url_for('admin.panel'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/panel')
@login_required
def panel():
    db, cursor = get_db()
    cursor.execute('SELECT * FROM workers WHERE verified_status = 0')
    unverified = cursor.fetchall()
    cursor.execute('SELECT * FROM workers WHERE verified_status = 1')
    verified = cursor.fetchall()
    cursor.execute('SELECT c.id, c.reason, c.submitted_on, w.name, w.id as worker_id FROM complaints c JOIN workers w ON c.worker_id = w.id ORDER BY c.submitted_on DESC')
    complaints = cursor.fetchall()
    return render_template('admin/admin_panel.html', unverified=unverified, verified=verified, complaints=complaints)

@admin_bp.route('/verify/<int:worker_id>')
@login_required
def verify_worker(worker_id):
    db, cursor = get_db()
    cursor.execute('SELECT * FROM workers WHERE id = %s', (worker_id,))
    worker = cursor.fetchone()
    return render_template('admin/verify.html', worker=worker)

@admin_bp.route('/approve/<int:worker_id>', methods=['POST'])
@login_required
def approve_worker(worker_id):
    db, cursor = get_db()
    cursor.execute('UPDATE workers SET verified_status = 1 WHERE id = %s', (worker_id,))
    db.commit()
    flash(f'Worker ID {worker_id} has been approved.', 'success')
    return redirect(url_for('admin.panel'))

@admin_bp.route('/reject/<int:worker_id>', methods=['POST'])
@login_required
def reject_worker(worker_id):
    db, cursor = get_db()
    cursor.execute('SELECT aadhaar_path, rationcard_path, selfie_path FROM workers WHERE id = %s', (worker_id,))
    worker = cursor.fetchone()
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if worker:
        for file_path in worker.values():
            if file_path:
                # Ensure OS path compatibility even if forward slashes are used in DB
                local_file_path = os.path.join(upload_folder, *file_path.split('/'))
                try:
                    os.remove(local_file_path)
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")

    cursor.execute('DELETE FROM workers WHERE id = %s', (worker_id,))
    db.commit()
    flash(f'Worker ID {worker_id} has been rejected and deleted.', 'warning')
    return redirect(url_for('admin.panel'))

@admin_bp.route('/toggle_block/<int:worker_id>', methods=['POST'])
@login_required
def toggle_block(worker_id):
    db, cursor = get_db()
    cursor.execute('SELECT is_blocked FROM workers WHERE id = %s', (worker_id,))
    worker = cursor.fetchone()
    if worker:
        new_status = 1 - worker['is_blocked']
        cursor.execute('UPDATE workers SET is_blocked = %s WHERE id = %s', (new_status, worker_id))
        db.commit()
        action = "blocked" if new_status == 1 else "unblocked"
        flash(f'Worker ID {worker_id} has been {action}.', 'success')
    return redirect(url_for('admin.panel'))

@admin_bp.route('/delete_complaint/<int:complaint_id>', methods=['POST'])
@login_required
def delete_complaint(complaint_id):
    db, cursor = get_db()
    cursor.execute('DELETE FROM complaints WHERE id = %s', (complaint_id,))
    db.commit()
    flash('Complaint has been deleted.', 'success')
    return redirect(url_for('admin.panel'))
