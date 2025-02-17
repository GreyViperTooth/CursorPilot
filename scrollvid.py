import cv2
import dlib
import pyautogui
import time
import numpy as np
import pygetwindow as gw

# Initialize face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Thresholds for detecting tilt angles
DOWNWARD_TILT_THRESHOLD = 105  # Angle for downward tilt
UPWARD_TILT_THRESHOLD = 80  # Angle for upward tilt

# Scrolling settings
SCROLL_SPEED = 50  # Pixels to scroll per interval
SCROLL_INTERVAL = 0.1  # Time between scroll actions

# Video control settings
ACTION_INTERVAL = 0.2  # Interval for triggering video controls

# State variables to prevent repeated actions
last_action_time = time.time()
last_scroll_time = time.time()

# Calculate angle between two points (nose and chin)
def calculate_angle(p1, p2):
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    angle = np.arctan2(delta_y, delta_x) * (180.0 / np.pi)  # Convert radians to degrees
    return angle

# Check if the current window is in fullscreen mode
def is_fullscreen():
    windows = gw.getWindowsWithTitle("")  # Retrieve all windows
    for win in windows:
        if win.isMaximized and win.width == screen_width and win.height == screen_height:
            return True
    return False

# Main function for real-time control
def main():
    global last_action_time, last_scroll_time
    cap = cv2.VideoCapture(0)  # Open the webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)  # Get facial landmarks

            # Extract key points: nose tip and chin
            nose_point = (landmarks.part(30).x, landmarks.part(30).y)
            chin_point = (landmarks.part(8).x, landmarks.part(8).y)

            # Calculate the tilt angle
            tilt_angle = calculate_angle(nose_point, chin_point)

            # Display debugging info (points and angle)
            cv2.circle(frame, nose_point, 5, (0, 255, 0), -1)
            cv2.circle(frame, chin_point, 5, (255, 0, 0), -1)
            cv2.putText(frame, f"Tilt Angle: {tilt_angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # If fullscreen, control video playback
            if is_fullscreen():
                current_time = time.time()
                if tilt_angle > DOWNWARD_TILT_THRESHOLD:
                    if current_time - last_action_time > ACTION_INTERVAL:
                        pyautogui.press("right")  # Fast forward
                        last_action_time = current_time
                        cv2.putText(frame, "Fast Forward", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                elif tilt_angle < UPWARD_TILT_THRESHOLD:
                    if current_time - last_action_time > ACTION_INTERVAL:
                        pyautogui.press("left")  # Reverse
                        last_action_time = current_time
                        cv2.putText(frame, "Reverse", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                # In normal mode, control scrolling
                current_time = time.time()
                if current_time - last_scroll_time > SCROLL_INTERVAL:
                    if tilt_angle > DOWNWARD_TILT_THRESHOLD:
                        pyautogui.scroll(-SCROLL_SPEED)  # Scroll down
                        cv2.putText(frame, "Scrolling Down", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    elif tilt_angle < UPWARD_TILT_THRESHOLD:
                        pyautogui.scroll(SCROLL_SPEED)  # Scroll up
                        cv2.putText(frame, "Scrolling Up", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    last_scroll_time = current_time

        # Display the video frame
        cv2.imshow("Head-Based Control", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()