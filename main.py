import os
from src.extract_frames import extract_frames
from src.detect_ball import detect_ball
from src.track_ball import calculate_speed
from src.api import app

if __name__ == "__main__":
    print("🚀 Running MLB Statcast Extraction...")
    os.system("flask run")