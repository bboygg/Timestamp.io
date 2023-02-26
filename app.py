# Copyright (c) 2023, bboygg
# All rights reserved.

import os 
from flask import Flask, flash, request, redirect, send_from_directory, url_for, render_template
from werkzeug.utils import secure_filename
import secrets
import cv2
from datetime import datetime


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
#@app.route('/uploads/<filename>')
# def download_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return render_template('download.html',filename=filename)

@app.route('/video_timestamped/<filename>')
def download_processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True )
    

'''Initial page prompt user to upload file and (display) and download '''
@app.route('/', methods=['GET', 'POST'])
def upload_video():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        file = request.files['filename']

        # If the user does not select a file, the browser throw notification
        if file.filename == '':
            flash('No Selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            # check your filename is secure
            filename = secure_filename(file.filename)
            
            # set filepath and save it into uploads folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create a video capture object for the uploaded file
            cap = cv2.VideoCapture(file_path)

            # Get the frames per second (FPS) of the video and video properties
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            output_folder = "video_timestamped"
            if not os.path.exists(output_folder):
                os.mkdir(output_folder)
            
            app.config['PROCESSED_FOLDER'] = output_folder


            #postfix = "_timestamped"
            #filename_processed = filename.rsplit('.', 1)[0] + postfix + '.' + filename.rsplit('.', 1)[1]

            # Define output path
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], f"timestamped_{filename}")
            
            
            # Create video_writer to save the video file
            video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            # Get the total number of frames in the video
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_count = 0

             # putText variables
            text = 'Time remaining: '
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (10, 70)
            fontScale = 3.0
            color = (0,165,255)
            thickness = 3

            # Loop through each frame of the video 
            while True: 
                # Read the next frame
                ret, frame = cap.read()
                
                # If there are no more frames, break out of the loop
                if not ret: 
                    break

                # Calculate the reamining time in seconds
                time = (total_frames - frame_count) / fps

                # Convert time to datetime format
                m,s = divmod(time, 60)
                time = "{:0>2}:{:05.2f}".format(int(m), s)

                # Add the remaining time to the frame
                cv2.putText(frame, text + f"{time}", org, font, fontScale, color, thickness)

                # Wrtie the frame to the output video
                video_writer.write(frame)

                # Increase the frame count
                frame_count += 1
            # Release the video capture object
            video_writer.release()
            cap.release()
            
            return redirect(url_for('download_file', filename=f"timestamped_{filename}"))
        return redirect("/")
    

# The app will be running in debug mode, so any error messages or output will be displayed in the console.
if __name__ == '__main__':
    app.run(debug=True)