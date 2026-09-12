import cv2
import os
import sys
import random

def extract_frames(video_path, output_dir, target_size=(1024, 1024), frames_per_second=1):
    """
    Extracts a specified number of random frames per second from a video file,
    crops them to a target size, and saves them as individual images.  Includes a progress counter.

    Args:
        video_path (str): The path to the video file.
        output_dir (str): The path to the directory where frames will be saved.
        target_size (tuple, optional): The desired size of the cropped frames (width, height).
            Defaults to (1024, 1024).
        frames_per_second (int, optional): The number of random frames to extract per second.
            Defaults to 3.
    """
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        sys.exit(1)

    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))  # Get the video's frame rate
    if frame_rate <= 0:
        print("Error: Could not determine video frame rate.  Defaulting to 30 FPS, which may cause incorrect sampling.")
        frame_rate = 30

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        print("Error: Could not determine total number of frames. Progress counter may be inaccurate.")
        total_frames = 0

    frame_count = 0
    saved_frame_count = 0
    while True:
        # Read the next frame from the video
        ret, frame = cap.read()

        # If we've reached the end of the video, exit the loop
        if not ret:
            break

        # Calculate if this frame should be considered for extraction
        second = frame_count // frame_rate  # Get the second number
        frame_within_second = frame_count % frame_rate  # Frame position within the second.

        if frame_within_second in random.sample(range(frame_rate), frames_per_second):
            # Get the original frame dimensions
            height, width = frame.shape[:2]

            # Calculate the crop coordinates to center the crop
            x1 = (width - target_size[0]) // 2
            y1 = (height - target_size[1]) // 2
            x2 = x1 + target_size[0]
            y2 = y1 + target_size[1]

            # Crop the frame to the target size
            frame_cropped = frame[y1:y2, x1:x2]

            # Construct the output path for the frame
            frame_filename = os.path.join(output_dir, f"{saved_frame_count:06d}.jpg")  # Use jpg
            # Save the cropped frame as an image
            cv2.imwrite(frame_filename, frame_cropped)
            # print(f"Saved frame: {frame_filename}")
            saved_frame_count += 1

        frame_count += 1

        # Calculate and print progress
        if total_frames > 0 and frame_count % 100 == 0:  # Update progress every 100 frames
            progress = (frame_count / total_frames) * 100
            print(f"Processed {frame_count}/{total_frames} frames ({progress:.2f}%)")
        elif total_frames == 0 and frame_count % 100 == 0:
             print(f"Processed {frame_count} frames") #when total frames is unknown


    # Release the video capture object
    cap.release()
    print(
        f"Successfully extracted {saved_frame_count} frames ({frames_per_second} random frames per second) to {output_dir} with size {target_size}"
    )
    return saved_frame_count



if __name__ == "__main__":
    # Specify the path to your video file
    video_path = "CitiesSkylines2_Data.mkv"  # Replace with the actual path to your video file

    # Specify the directory where you want to save the frames
    output_dir = "./dataset/images"  # The directory will be created if it does not exist.

    # Specify the target size for the cropped frames
    target_size = (1024, 1024)  # Width, Height

    # Specify the number of random frames per second
    frames_per_second = 3

    # Extract the frames
    extracted_frame_count = extract_frames(video_path, output_dir, target_size, frames_per_second)
    print(f"Total frames extracted: {extracted_frame_count}")
