from flask import Blueprint, render_template

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/upload-gpl')
def upload_gpl():
    return render_template('upload_gpl.html')

@main_routes.route('/upload-mo')
def upload_mo():
    return render_template('upload_mo.html')