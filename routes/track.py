# lwms/routes/track.py
import os
from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app import get_db
from utils.validation import allowed_file

track_bp = Blueprint('track', __name__)

@track_bp.route('/track/add/<int:worker_id>', methods=['GET', 'POST'])
def add_work_log(worker_id):
    db, cursor = get_db()
    cursor.execute("SELECT id, name FROM workers WHERE id = %s", (worker_id,))
    worker = cursor.fetchone()

    if not worker:
        flash('Worker not found.', 'danger')
        return redirect(url_for('search.search'))

    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        before_img = request.files['before_work_image']
        after_img = request.files['after_work_image']

        if not before_img or not after_img or not rating:
            flash('Before/After images and a rating are required.', 'danger')
            return render_template('track_work.html', worker=worker)
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        before_path, after_path = None, None

        if before_img and allowed_file(before_img.filename, allowed_extensions):
            filename = secure_filename(f"before_{worker_id}_{date.today().strftime('%Y%m%d%H%M%S')}.jpg")
            before_path = os.path.join('before_work', filename)
            before_img.save(os.path.join(upload_folder, before_path))

        if after_img and allowed_file(after_img.filename, allowed_extensions):
            filename = secure_filename(f"after_{worker_id}_{date.today().strftime('%Y%m%d%H%M%S')}.jpg")
            after_path = os.path.join('after_work', filename)
            after_img.save(os.path.join(upload_folder, after_path))

        if before_path and after_path:
            cursor.execute(
                "INSERT INTO work_logs (worker_id, work_date, before_work_image_path, after_work_image_path, rating, comments) VALUES (%s, %s, %s, %s, %s, %s)",
                (worker_id, date.today(), before_path, after_path, rating, comments)
            )
            db.commit()
            flash('Work log and rating submitted successfully!', 'success')
            return redirect(url_for('track.view_work_history', worker_id=worker_id))
        else:
            flash('There was an error uploading the images.', 'danger')

    return render_template('track_work.html', worker=worker)

@track_bp.route('/track/history/<int:worker_id>')
def view_work_history(worker_id):
    db, cursor = get_db()
    cursor.execute("SELECT id, name, phone, work_type FROM workers WHERE id = %s", (worker_id,))
    worker = cursor.fetchone()

    if not worker:
        flash('Worker not found.', 'danger')
        return redirect(url_for('search.search'))

    cursor.execute("SELECT * FROM work_logs WHERE worker_id = %s ORDER BY work_date DESC", (worker_id,))
    logs = cursor.fetchall()
    
    cursor.execute("SELECT AVG(rating) as avg_rating FROM work_logs WHERE worker_id = %s", (worker_id,))
    avg_rating_result = cursor.fetchone()
    avg_rating = avg_rating_result['avg_rating'] if avg_rating_result and avg_rating_result['avg_rating'] else 0
    
    return render_template('worker_history.html', worker=worker, logs=logs, avg_rating=avg_rating)