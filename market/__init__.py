from flask import Flask
# from routes.main_routes import main_routes
# from routes.file_routes import file_routes
import logging
from logging.handlers import RotatingFileHandler
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

# Set up logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/audit_tool.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Audit Tool startup')

from market import routes