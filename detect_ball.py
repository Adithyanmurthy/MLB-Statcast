import cv2
import numpy as np
import os

def detect_ball(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        print(f" ERROR: Unable to load image {image_path}")
        return None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the color range for white baseball detection
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 30, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Debugging: Show mask image
    cv2.imshow("Ball Mask", mask)
    cv2.waitKey(100)  # Display for 100ms (press 'q' to exit)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"⚠️ No ball detected in {image_path}")
        return None

    for contour in contours:
        if cv2.contourArea(contour) > 50:  # Ignore small objects
            x, y, w, h = cv2.boundingRect(contour)
            print(f" Ball detected at ({x + w//2}, {y + h//2}) in {image_path}")
            return (x + w//2, y + h//2)

    print(f"⚠️ No ball found in {image_path}")
    return None

# Run detection on a sample frame
sample_frame = "data/frames/frame_7950.jpg"
detect_ball(sample_frame)