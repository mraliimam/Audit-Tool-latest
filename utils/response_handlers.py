from flask import jsonify, send_file
import os

def handle_file_upload_error(error_type):
    error_messages = {
        'no_file': 'No file uploaded',
        'no_file_selected': 'No file selected',
        'invalid_format': 'Invalid file format. Only Excel files (.xlsx, .xls) are allowed',
        'processing_failed': 'Processing failed'
    }
    return jsonify({'error': error_messages.get(error_type, 'Unknown error')}), 400

def handle_processed_file():
    if os.path.exists('files.zip'):
        return send_file('files.zip', as_attachment=True)
    return jsonify({'error': 'Processing failed'}), 500