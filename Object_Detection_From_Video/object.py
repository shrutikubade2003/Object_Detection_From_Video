import os
import cv2

# Function to check if file exists before processing
def check_file_existence(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    return True

# Function to create output directory if it doesn't exist
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to extract frames from a video, now saving them in unique directories
def extract_frames_from_video(video_path, output_base_dir, frame_rate=1):
    if not check_file_existence(video_path):
        return
    
    # Create a unique directory for each video based on its name
    video_name = os.path.splitext(os.path.basename(video_path))[0]  # Get video file name without extension
    output_dir = os.path.join(output_base_dir, video_name)
    create_dir(output_dir)
    
    # Capture the video from file
    vidcap = cv2.VideoCapture(video_path)
    
    if not vidcap.isOpened():
        print(f"Failed to open video file: {video_path}")
        return
    
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # Get frames per second of the video
    count = 0
    success = True
    
    # Extract frames
    while success:
        success, frame = vidcap.read()
        if success and count % (fps * frame_rate) == 0:
            frame_filename = f"{video_name}_frame_{count}.jpg"
            frame_path = os.path.join(output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            print(f"Saved {frame_filename}")
        
        count += 1
    
    vidcap.release()

# Function to extract a single frame from a photo
def extract_frame_from_photo(photo_path, output_base_dir):
    if not check_file_existence(photo_path):
        return
    
    # Create a unique directory for photos if necessary
    create_dir(output_base_dir)
    
    img = cv2.imread(photo_path)
    if img is None:
        print(f"Error reading image from {photo_path}")
        return
    
    filename = os.path.basename(photo_path)
    output_path = os.path.join(output_base_dir, filename)
    cv2.imwrite(output_path, img)
    print(f"Saved {output_path}")

# Function to list all files in a directory with specified extensions
def list_files_in_directory(directory, extensions):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return []
    
    files = [f for f in os.listdir(directory) if f.lower().endswith(extensions)]
    if not files:
        print(f"No files with extensions {extensions} found in {directory}")
    return files

# Example usage for video
video_dir = r'F:\object_detection\ml_data'
output_dir_for_video = 'video_frames'
video_extensions = ('.mp4', '.avi', '.mkv')  # Add video file extensions to be processed

video_files = list_files_in_directory(video_dir, video_extensions)

# Process all videos in the folder
for video_file in video_files:
    video_path = os.path.join(video_dir, video_file)
    extract_frames_from_video(video_path, output_dir_for_video, frame_rate=1)

# Example usage for photo
photo_dir = r'F:\object_detection\ml_images'
output_dir_for_photo = 'photo_frames'
image_extensions = ('.jpg', '.jpeg', '.png')  # Add image file extensions to be processed

photo_files = list_files_in_directory(photo_dir, image_extensions)

# Process all photos in the folder
for photo_file in photo_files:
    photo_path = os.path.join(photo_dir, photo_file)
    extract_frame_from_photo(photo_path, output_dir_for_photo)
