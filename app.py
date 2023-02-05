from flask import Flask, render_template, request, send_file, send_from_directory, url_for
from flask_uploads import UploadSet, AUDIO, configure_uploads, ALL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from utils import generate_timestamp


# Configure application"
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ALLOWED_EXTENSIONS = {'mp4', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configure upload video
videos = UploadSet('videos', AUDIO)
configure_uploads(app, videos)

# send fiel to directory
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


'''Initial page prompt user to upload file and (display) and download '''
@app.route('/', methods=['GET', 'POST'])
def upload_video():
    form = UploadForm()
    if form.validate_on_submit(): 
        fielname = videos.save(form.video.data)
        file_url = url_for('get_file', filename=fielname)
    else:
        file_url = None

    return render_template('index.html', form=form, file_url=file_url)


    
''' upload form class'''
class UploadForm(FlaskForm):
    video = FileField(
        validators=[
            FileAllowed(videos, 'Only video are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    #submit button text
    submit = SubmitField('Upload')



if __name__ == '__main__':
    app.run(debug=True)