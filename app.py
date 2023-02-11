# Copyright (c) 2023, bboygg
# All rights reserved.

import os 
from flask import Flask, flash, request, redirect, send_from_directory, url_for, render_template
from werkzeug.utils import secure_filename
import secrets
from utils import generate_timestamp



# Configure application"
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ALLOWED_EXTENSIONS = {'mp4'}
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


''' check if an extension is valid ''' 
# If the extension is in the list, the function returns True, else the functions returns 'False'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# send file to directory
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


'''Initial page prompt user to upload file and (display) and download '''
@app.route('/', methods=['GET', 'POST'])
def upload_video():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        file = request.files['filename']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No Selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            generate_timestamp(filename)
            return redirect(url_for('download_file', filename=filename))
        return redirect("/")
    

# The app will be running in debug mode, so any error messages or output will be displayed in the console.
if __name__ == '__main__':
    app.run(debug=True)