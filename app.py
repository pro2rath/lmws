# lwms/app.py
import os
import mysql.connector
from flask import Flask, g, current_app, send_from_directory

# --- Database Setup (Updated for MySQL) ---
def get_db():
    """Connect to the application's configured MySQL database."""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        # The cursor is what executes queries. 'dictionary=True' is crucial!
        # It makes the results act like Python dictionaries.
        g.c = g.db.cursor(dictionary=True, buffered=True)
    return g.db, g.c

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Teardown app context to close the database connection
    @app.teardown_appcontext
    def close_connection(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    # --- Register Blueprints ---
    from routes.register import register_bp
    from routes.search import search_bp
    from routes.daily import daily_bp
    from routes.complaint import complaint_bp
    from routes.admin import admin_bp
    from routes.track import track_bp

    app.register_blueprint(register_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(daily_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(track_bp)

    # --- Main & Static Routes ---
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    @app.route('/privacy')
    def privacy_policy():
        from flask import render_template
        return render_template('privacy_policy.html')

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serves files from the UPLOAD_FOLDER."""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)