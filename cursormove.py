import cv2
import dlib
import pyautogui
import numpy as np

# Initialize face detector and predictor
# Detector identifies faces, and predictor maps facial landmarks

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Screen dimensions for cursor movement coordination
screen_width, screen_height = pyautogui.size()

# Constants for movement scaling and sensitivity
SCALING_FACTOR = 1.5  # Amplify head movement
MOVEMENT_THRESHOLD = 10  # Minimum movement in pixels to adjust the cursor

# Helper function: Calculates the center of a rectangle (e.g., a face region)
def get_center(rect):
    return (rect.left() + rect.right()) // 2, (rect.top() + rect.bottom()) // 2

# Helper function: Maps a point to screen dimensions
# Converts facial feature coordinates to screen coordinates
def normalize_to_screen(x, y, frame_width, frame_height):
    screen_x = np.interp(x, [0, frame_width], [0, screen_width])
    screen_y = np.interp(y, [0, frame_height], [0, screen_height])
    return int(screen_x), int(screen_y)

# Main function: Tracks face movement to control the cursor
def main():
    cap = cv2.VideoCapture(0)  # Open the webcam
    prev_cursor_x, prev_cursor_y = pyautogui.position()  # Initialize cursor position tracking

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for natural interaction
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = detector(gray)
        for face in faces:
            # Visualize the detected face with a rectangle
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

            # Determine the face center
            face_center_x, face_center_y = get_center(face)

            # Map the face center to screen dimensions
            screen_x, screen_y = normalize_to_screen(face_center_x, face_center_y, frame.shape[1], frame.shape[0])

            # Compute movement deltas and scale appropriately
            delta_x = (screen_x - prev_cursor_x) * SCALING_FACTOR
            delta_y = (screen_y - prev_cursor_y) * SCALING_FACTOR

            # Only move the cursor if movement is significant
            if abs(delta_x) > MOVEMENT_THRESHOLD or abs(delta_y) > MOVEMENT_THRESHOLD:
                current_x, current_y = pyautogui.position()  # Get current cursor position
                new_x = current_x + delta_x
                new_y = current_y + delta_y

                # Clamp cursor position within screen bounds
                new_x = np.clip(new_x, 0, screen_width)
                new_y = np.clip(new_y, 0, screen_height)

                # Move the cursor to the new position
                pyautogui.moveTo(new_x, new_y)

                # Update previous cursor position for next iteration
                prev_cursor_x, prev_cursor_y = screen_x, screen_y

        # Display the video feed with visual overlays
        cv2.imshow("Head-Based Cursor Movement", frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
