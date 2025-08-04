# setup_db.py

from flask import Flask
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

def create_tables():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS lwms_db")
        mysql.connection.select_db('lwms_db')

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                phone VARCHAR(15),
                work_type VARCHAR(50),
                aadhaar_path VARCHAR(255),
                rationcard_path VARCHAR(255),
                selfie_path VARCHAR(255),
                is_verified BOOLEAN DEFAULT FALSE,
                is_blocked BOOLEAN DEFAULT FALSE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                worker_id INT,
                reason TEXT,
                FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE
            )
        """)

        mysql.connection.commit()
        print("✅ Tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == '__main__':
    create_tables()
