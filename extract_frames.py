import os
import cv2

def extract_frames(video_path, output_folder, frame_rate=30):
    if not os.path.exists(video_path):
        print(f"❌ ERROR: Video file not found at {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ ERROR: Unable to open video file {video_path}")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"🎥 Video Loaded: {video_path}")
    print(f"🎞️ Total Frames: {frame_count}, FPS: {fps}")

    count = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("❌ ERROR: No frames were read from the video. Possibly at the end.")
            break

        if count % frame_rate == 0:
            frame_path = f"{output_folder}/frame_{count}.jpg"
            cv2.imwrite(frame_path, frame)
            print(f"📸 Saved frame: {frame_path}")

        count += 1

    cap.release()
    print("✅ Frame extraction completed!")

# Use the new converted video
extract_frames("data/mlb_fixed.mp4", "data/frames", frame_rate=30)