from flask import Flask, render_template, request, send_file
from flask_uploads import UploadSet, AUDIO, configure_uploads, ALL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import cv2
import os

UPLOAD_FOLDER = 'static/'
# ALLOWED_EXTENSIONS = {'mp4', 'jpeg', 'gif'}


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

videos = UploadSet('videos', AUDIO)
configure_uploads(app, videos)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''Initial page prompt user to upload file and (display) and download '''
@app.route('/', method=['GET', 'POST'])
def index():
     if request.method == 'POST':
        # Get the uploaded video file
        video_file = request.files['video_file']

        # Save the video file to the server
        video_file.save('static/original_video.mp4')

        # Open the video file
        cap = cv2.VideoCapture('static/original_video.mp4')

        # Get the frames per second (FPS) of the video
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Define the codec and create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('static/modified_video.mp4', fourcc, fps, (640,480))

        # Loop through each frame of the video
        frame_count = 0
        while True:
            # Read the next frame
            ret, frame = cap.read()

            # If there are no more frames, break out of the loop
            if not ret:
                break

            # resize the frame
            frame = cv2



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