import cv2
import numpy as np

# List to store the coordinates of the points you click
clicked_points = []

# Mouse callback function to record coordinates
def get_coordinates(event, x, y, flags, param):
    """
    Callback function to get pixel coordinates on mouse click.
    Appends the clicked (x, y) coordinates to the 'clicked_points' list.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"Clicked coordinates: ({x}, {y})")
        # Optionally, draw a small circle on the displayed frame to visualize the clicked point
        # cv2.circle(param['frame'], (x, y), 5, (0, 255, 0), -1)
        # cv2.imshow(param['window_name'], param['frame'])

# --- Video file and settings ---
video_path = 'output_video (2).mp4'
window_name = 'Select Zone Points'

# --- Load the video and read a frame for selection ---
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    # Handle the error, perhaps exit the program
    exit()

# Read a frame (e.g., the first frame) to display for point selection
success, display_frame = cap.read()

if not success:
    print("Error: Could not read frame from video")
    cap.release()
    exit()

# Get video resolution (confirming it's 1024x1024 as expected)
# frame_height, frame_width = display_frame.shape[:2]
# print(f"Video resolution: {frame_width}x{frame_height}")

# Create a window and set the mouse callback function
cv2.namedWindow(window_name)
# Pass the frame and window name to the callback if you want to draw on it
# cv2.setMouseCallback(window_name, get_coordinates, param={'frame': display_frame, 'window_name': window_name})
cv2.setMouseCallback(window_name, get_coordinates)


print(f"Displaying a frame from '{video_path}' ({display_frame.shape[1]}x{display_frame.shape[0]}).")
print("Click on the points in the window to get their pixel coordinates.")
print("Press any key on the keyboard when you are finished selecting points.")

# Display the frame and wait for mouse clicks and a key press to exit
cv2.imshow(window_name, display_frame)
cv2.waitKey(0) # Wait indefinitely until a key is pressed

# --- Clean up resources ---
cv2.destroyWindow(window_name)
cap.release()

# --- Print the collected coordinates ---
print("\n--- Collected Coordinates ---")
if clicked_points:
    for i, point in enumerate(clicked_points):
        print(f"Point {i+1}: {point}")
else:
    print("No points were clicked.")

print("----------------------------")