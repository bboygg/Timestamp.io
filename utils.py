import cv2
import os
from datetime import datetime

def generate_timestamp(video):
    # Open the video file
    cap = cv2.VideoCapture(video)

    # Get the frames per second (FPS) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a folder to save the timestamped frames
    os.makedirs("video_timestamped", exist_ok=True)

    # Loop through each frame of the video
    frame_count = 0
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # If there are no more frames, break out of the loop
        if not ret:
            break

        # resize the frames
        frame = cv2.resize(frame, (640, 480))

        # Calculate the remaining time in seconds
        time = (total_frames - frame_count) / fps

        # convert time to datetime format
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        time = "{:0>2}:{:0>2}:{:05.2f}".format(int(h), int(m), s)

        # Add the remaining time to the frame
        cv2.putText(frame, f"{time}", (430, 450),
                    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (43, 165, 245), 2)

        # Save the frame with timestamp to the folder
        cv2.imwrite("./video_timestamped/frame_{frame_count}.jpg", frame)

        # Increase the frame count
        frame_count += 1

    # Release the video capture object
    cap.release()


