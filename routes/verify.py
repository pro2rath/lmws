# lwms/routes/verify.py
from flask import Blueprint

# The core verification logic (view, approve, reject) has been integrated
# into the admin blueprint (admin.py) to keep all admin actions centralized
# and protected by the same login decorator.

verify_bp = Blueprint('verify', __name__)

@verify_bp.route('/verification-info')
def info():
    return "Verification processes are handled in the Admin Panel."