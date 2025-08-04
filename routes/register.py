# lwms/routes/register.py
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app import get_db
from utils.validation import is_valid_aadhaar, allowed_file

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        work_type = request.form['work_type']
        location = request.form['location']
        aadhaar_number = request.form['aadhaar_number']

        selfie_file = request.files['selfie']
        aadhaar_file = request.files['aadhaar_file']
        rationcard_file = request.files.get('rationcard_file') # Optional

        if not all([name, phone, work_type, location, aadhaar_number, selfie_file]):
            flash('All fields marked with * are required.', 'danger')
            return render_template('register.html')

        if not is_valid_aadhaar(aadhaar_number):
            flash('Invalid Aadhaar number. Must be 12 digits.', 'danger')
            return render_template('register.html')

        db, cursor = get_db()
        cursor.execute('SELECT id FROM workers WHERE phone = %s', (phone,))
        if cursor.fetchone():
            flash('This phone number is already registered.', 'danger')
            return render_template('register.html')

        upload_folder = current_app.config['UPLOAD_FOLDER']
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        selfie_path, aadhaar_path, rationcard_path = None, None, None

        # Always use forward slashes in paths stored for web/DB use
        def to_web_path(path):
            return path.replace("\\", "/")

        # Selfie - Required
        if selfie_file and allowed_file(selfie_file.filename, allowed_extensions):
            selfie_filename = secure_filename(f"selfie_{phone}.jpg")
            selfie_subpath = os.path.join('selfies', selfie_filename)
            selfie_path = to_web_path(selfie_subpath)
            selfie_file.save(os.path.join(upload_folder, selfie_subpath))
        else:
            flash('A valid selfie image is required.', 'danger')
            return render_template('register.html')

        # Aadhaar - Required
        if aadhaar_file and allowed_file(aadhaar_file.filename, allowed_extensions):
            aadhaar_filename = secure_filename(f"aadhaar_{phone}.jpg")
            aadhaar_subpath = os.path.join('aadhaar', aadhaar_filename)
            aadhaar_path = to_web_path(aadhaar_subpath)
            aadhaar_file.save(os.path.join(upload_folder, aadhaar_subpath))

        # Ration Card - Optional
        if rationcard_file and rationcard_file.filename and allowed_file(rationcard_file.filename, allowed_extensions):
            rationcard_filename = secure_filename(f"ration_{phone}.jpg")
            rationcard_subpath = os.path.join('rationcard', rationcard_filename)
            rationcard_path = to_web_path(rationcard_subpath)
            rationcard_file.save(os.path.join(upload_folder, rationcard_subpath))

        cursor.execute(
            "INSERT INTO workers (name, phone, work_type, location, aadhaar_path, rationcard_path, selfie_path) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, phone, work_type, location, aadhaar_path, rationcard_path, selfie_path)
        )
        db.commit()

        flash('Registration successful! Your profile will be visible after admin approval.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')
