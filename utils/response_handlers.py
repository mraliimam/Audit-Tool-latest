from flask import jsonify, send_file
import os
from market import app

def handle_file_upload_error(error_type):
    error_messages = {
        'no_file': 'No file uploaded',
        'no_file_selected': 'No file selected',
        'invalid_format': 'Invalid file format. Only Excel files (.xlsx, .xls) are allowed',
        'processing_failed': 'Processing failed'
    }
    return jsonify({'error': error_messages.get(error_type, 'Unknown error')}), 400

def handle_processed_file():
    zip_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], 'files.zip')
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return jsonify({'error': 'Processing failed'}), 500