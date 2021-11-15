import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Blueprint

save_attachments_bp = Blueprint('save_attachments', __name__)
uploads_dir = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@save_attachments_bp.route('/save', methods=['GET', 'POST'])
def upload_file():
    files = request.files.values()
    print(files)
    for item in files:
        print(item)
    if 'attachment' not in request.files:
        print("1")
        flash('No file part')
    file = request.files['attachment']
    if file.filename == '':
        print("2")
        flash('No selected file')
    if file and allowed_file(file.filename):
        print("3")
        filename = secure_filename(file.filename)
        file.save(os.path.join(uploads_dir, filename))
    print("4")
    return "nic"

