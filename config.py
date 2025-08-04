# lwms/config.py
import os

# Application root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for session management. Change this to a random string.
SECRET_KEY = 'your-super-secret-key-change-me'

# --- NEW MYSQL CONFIG FOR XAMPP ---
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'  # Default XAMPP user
MYSQL_PASSWORD = ''  # Default XAMPP password is empty
MYSQL_DB = 'lwms1' # The database name we will create

# Uploads configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'