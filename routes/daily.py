# lwms/routes/daily.py
from flask import Blueprint, render_template, redirect, url_for, flash
from datetime import date
from app import get_db

daily_bp = Blueprint('daily', __name__)

@daily_bp.route('/daily')
def daily_view():
    today = date.today().isoformat()
    db, cursor = get_db()
    cursor.execute(
        "SELECT id, name, phone, work_type, location, selfie_path FROM workers WHERE verified_status = 1 AND is_blocked = 0 AND last_available_date = %s ORDER BY name",
        (today,)
    )
    workers = cursor.fetchall()
    return render_template('daily.html', workers=workers, today=today)

@daily_bp.route('/mark-available/<int:worker_id>')
def mark_available(worker_id):
    today = date.today().isoformat()
    db, cursor = get_db()
    cursor.execute('SELECT id FROM workers WHERE id = %s', (worker_id,))
    if cursor.fetchone():
        cursor.execute('UPDATE workers SET last_available_date = %s WHERE id = %s', (today, worker_id))
        db.commit()
        flash('You have been marked as available for today!', 'success')
    else:
        flash('Worker not found.', 'danger')
    return redirect(url_for('search.search'))