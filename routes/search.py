# lwms/routes/search.py
from flask import Blueprint, render_template, request
from app import get_db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    db, cursor = get_db()
    query = "SELECT id, name, phone, work_type, location, selfie_path FROM workers WHERE verified_status = 1 AND is_blocked = 0"
    params = []
    
    if request.method == 'POST':
        work_type = request.form.get('work_type')
        location = request.form.get('location')
        
        if work_type:
            query += " AND work_type = %s"
            params.append(work_type)
        if location:
            query += " AND location LIKE %s"
            params.append(f"%{location}%")

    cursor.execute(query, params)
    workers = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT work_type FROM workers WHERE verified_status = 1 ORDER BY work_type")
    work_types = cursor.fetchall()
    cursor.execute("SELECT DISTINCT location FROM workers WHERE verified_status = 1 ORDER BY location")
    locations = cursor.fetchall()

    return render_template('search.html', workers=workers, work_types=work_types, locations=locations)