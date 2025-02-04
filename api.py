from extract_frames import extract_frames
from detect_ball import detect_ball
from track_ball import calculate_speed
import os
import cv2
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_video():
    video = request.files["file"]
    video_path = "data/mlb_game.mp4"
    video.save(video_path)
    extract_frames(video_path, "data/frames")
    frame_1 = detect_ball("data/frames/frame_30.jpg")
    frame_2 = detect_ball("data/frames/frame_60.jpg")
    pitch_speed = calculate_speed(frame_1, frame_2, 1/30)
    return jsonify({"pitch_speed": pitch_speed})

if __name__ == "__main__":
    app.run(debug=True)