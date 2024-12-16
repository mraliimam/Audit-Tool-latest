from flask import request , render_template
from utils.file_handlers import allowed_file, save_uploaded_file
from utils.response_handlers import handle_file_upload_error, handle_processed_file
from market import app
from market.static.scripting import goldenFile
from market.static.mo import moFile

import os

def clear_uploads_folder():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            app.logger.error(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/')
def home():
    clear_uploads_folder()
    return render_template('home.html')

@app.route('/upload-gpl')
def upload_gpl():
    clear_uploads_folder()
    return render_template('upload_gpl.html')

@app.route('/upload-mo')
def upload_mo():
    clear_uploads_folder()
    return render_template('upload_mo.html')

@app.route('/process-gpl', methods=['POST'])
def process_gpl():
    if 'file' not in request.files:
        return handle_file_upload_error('no_file')
    
    file = request.files['file']
    if file.filename == '':
        return handle_file_upload_error('no_file_selected')
    
    if not allowed_file(file.filename):
        return handle_file_upload_error('invalid_format')
    
    filepath = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
    if not filepath:
        return handle_file_upload_error('processing_failed')
    
    try:
        app.logger.info(f"Processing file at {filepath}")
        flag = goldenFile(filepath)

        app.logger.info("File processed successfully")
    except Exception as e:
        app.logger.error(f"Error processing file: {e}")
        return handle_file_upload_error('processing_failed')
    
    return handle_processed_file()

@app.route('/process-mo', methods=['POST'])
def process_mo():
    if 'file' not in request.files:
        return handle_file_upload_error('no_file')
    
    file = request.files['file']
    if file.filename == '':
        return handle_file_upload_error('no_file_selected')
    
    if not allowed_file(file.filename):
        return handle_file_upload_error('invalid_format')
    
    filepath = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
    if not filepath:
        return handle_file_upload_error('processing_failed')
    
    moFile(filepath)
    
    return handle_processed_file()