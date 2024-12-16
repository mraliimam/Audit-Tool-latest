from flask import Blueprint, request, current_app
from utils.file_handlers import allowed_file, save_uploaded_file
from utils.response_handlers import handle_file_upload_error, handle_processed_file

file_routes = Blueprint('file_routes', __name__)

@file_routes.route('/process-gpl', methods=['POST'])
def process_gpl():
    if 'file' not in request.files:
        return handle_file_upload_error('no_file')
    
    file = request.files['file']
    if file.filename == '':
        return handle_file_upload_error('no_file_selected')
    
    if not allowed_file(file.filename):
        return handle_file_upload_error('invalid_format')
    
    filepath = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
    if not filepath:
        return handle_file_upload_error('processing_failed')
    
    # Import and run the GPL processing script
    from scripting import process_file
    process_file(filepath)
    
    return handle_processed_file()

@file_routes.route('/process-mo', methods=['POST'])
def process_mo():
    if 'file' not in request.files:
        return handle_file_upload_error('no_file')
    
    file = request.files['file']
    if file.filename == '':
        return handle_file_upload_error('no_file_selected')
    
    if not allowed_file(file.filename):
        return handle_file_upload_error('invalid_format')
    
    filepath = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
    if not filepath:
        return handle_file_upload_error('processing_failed')
    
    # Import and run the MO processing script
    from mo import processFile
    processFile(filepath)
    
    return handle_processed_file()