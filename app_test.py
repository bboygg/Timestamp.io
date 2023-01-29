from flask import Flask, render_template, send_from_directory, url_for

from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234qwer'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

''' send file to directory??'''
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

''' initial page prompt user to upload file and display'''
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url= url_for('get_file', filename=filename)
    else:
        file_url = None
        
    return render_template('index.html', form=form, file_url=file_url)


@app.route("/video")
def serve_video():
    # Open the video file
    video_capture = cv2.VideoCapture("video.mp4")
    
    # Get the frame rate
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    while True:
        # Read the next frame
        ret, frame = video_capture.read()
        
        # Check if the video has ended
        if not ret:
            break
        
        # Get the current frame number
        current_frame = video_capture.get(cv2.CAP_PROP_POS_FRAMES)
        
        # Calculate the playback time in seconds
        playback_time = current_frame / fps
        
        # Overlay the playback time on the frame
        cv2.putText(frame, f"{playback_time:.2f} sec", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Encode the frame as a JPEG image
        ret, jpeg = cv2.imencode(".jpg", frame)
        
        # Return the JPEG image to the client
        return send_file(io.BytesIO(jpeg.tobytes()), mimetype="image/jpeg")



''' upload form class'''
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ] 
    )
    
    #submit button text
    submit = SubmitField('Upload')


if __name__ == '__main__':
    app.run(debug=True)