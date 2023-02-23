import cv2
import os
from datetime import datetime

# Open the video file
'''
TODO: Implement path for video capture
'''
cap = cv2.VideoCapture("uploads")

# Get the frames per second (FPS) of the video and video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_folder = "video_timestamped"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
'''
TODO: Implement targeting mp4 file
'''

output_path = os.path.join(output_folder, "")
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_count = 0

# putText variables
text = 'Remaining Time: '
font = cv2.FONT_HERSHEY_SIMPLEX
org = (10, 70)
fontScale = 3.0
color = (0,165,255)
thickness = 3


'''
TODO: Implement into app.py
'''

# Loop through each frame of the video
while True:
    # Read the next frame
    ret, frame = cap.read()

    # If there are no more frames, break out of the loop
    if not ret:
        break

    # Calculate the remaining time in seconds
    time = (total_frames - frame_count) / fps

    # convert time to datetime format
    m, s = divmod(time, 60)
    time = "{:0>2}:{:05.2f}".format(int(m), s)


    
    # Add the remaining time to the frame
    cv2.putText(frame, text + f"{time}", org,
                font, fontScale, color, thickness)


    # Write the frame to the output video
    video_writer.write(frame)


    # Wait for a key press
    if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
        break

    # Increase the frame count
    frame_count += 1

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()