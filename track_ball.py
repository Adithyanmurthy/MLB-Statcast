import os
import cv2
import numpy as np

def detect_ball(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"ERROR: Unable to load image {image_path}")
        return None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 40, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    for contour in contours:
        if cv2.contourArea(contour) > 50:  # Ignore small objects
            x, y, w, h = cv2.boundingRect(contour)
            return (x + w//2, y + h//2)

    return None

def calculate_speed(position1, position2, time_diff):
    if position1 is None or position2 is None:
        return None

    distance = np.linalg.norm(np.array(position2) - np.array(position1))  # Distance in pixels

    # ⚡ Fixing Unrealistic Speed
    # Approximate field-of-view conversion: 1 pixel ~ 0.02 feet
    feet_per_pixel = 0.02  
    distance_in_feet = distance * feet_per_pixel

    # Convert to mph: Speed (feet/sec) * (3600 sec / 5280 feet)
    speed_mph = (distance_in_feet / time_diff) * (3600 / 5280)  

    return round(speed_mph, 2)  # Round to 2 decimal places

# Get list of frames
frame_folder = "data/frames"
frame_files = sorted([f for f in os.listdir(frame_folder) if f.endswith(".jpg")])

print(" Tracking Ball Movement...")
previous_position = None
frame_gap = 30  # Process every 30th frame

for i in range(0, len(frame_files) - frame_gap, frame_gap):
    frame_path_1 = os.path.join(frame_folder, frame_files[i])
    frame_path_2 = os.path.join(frame_folder, frame_files[i + frame_gap])

    position1 = detect_ball(frame_path_1)
    position2 = detect_ball(frame_path_2)

    if position1 and position2:
        speed = calculate_speed(position1, position2, 1/30)  # 30 FPS
        print(f" {frame_files[i]}: Ball at {position1}")
        print(f" {frame_files[i+frame_gap]}: Ball at {position2}")
        print(f" Estimated Pitch Speed: {speed} mph")
        previous_position = position2
    else:
        print(f"⚠️ No ball detected in {frame_files[i]} or {frame_files[i+frame_gap]}")

print(" Ball Tracking Completed!")