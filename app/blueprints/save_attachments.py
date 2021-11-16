import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Blueprint

save_attachments_bp = Blueprint('save_attachments', __name__)


def allowed_file(filename):
    valid_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in valid_extensions


@save_attachments_bp.route('/save', methods=['GET', 'POST'])
def upload_file():
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    files = request.files.getlist('attachment')
    print(files)
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(uploads_dir, filename)
            file.save(filepath)
    return "nic"

