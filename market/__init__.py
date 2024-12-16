from flask import Flask
# from routes.main_routes import main_routes
# from routes.file_routes import file_routes
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Register blueprints
# app.register_blueprint(main_routes)
# app.register_blueprint(file_routes, url_prefix='/file')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from market import routes