# CursorPilot

This project enables hands-free control of your computer using head movements. It includes two primary features: cursor movement and head-tilt-based scrolling and video playback. A graphical user interface (GUI) makes it easy to start, stop, and switch between features.

---

## Features

1. **Cursor Movement**
   - Controls the mouse cursor using head movements detected via a webcam.
   
2. **Scroll & Video Playback**
   - Scrolls pages or controls video playback based on head tilt angles.

3. **GUI Interface**
   - Simple GUI to select and run features.

---

## Requirements

- Python 3.7 or above
- Webcam (integrated or external)

### Required Python Libraries

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- OpenCV
- dlib
- numpy
- pyautogui
- pygetwindow
- tkinter (comes pre-installed with Python)

---

## Setup

1. **Download Required Files**
   - Ensure `shape_predictor_68_face_landmarks.dat` is in the project directory. Download it from [dlib's model repository](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
   
   Extract the `.bz2` file if necessary.

2. **Folder Structure**

   The project folder should contain:
   ```
   - shape_predictor_68_face_landmarks.dat
   - eye_track.py
   - scrollvid.py
   - GUIapp.py
   - requirements.txt
   ```

---

## Usage

### 1. Start the Application

Run the `GUIapp.py` file:

```bash
python GUIapp.py
```

### 2. Using the GUI

- **Cursor Movement**: Starts head-based cursor control.
- **Scroll & Video Playback**: Activates head-tilt scrolling or video control.
- **Stop Feature**: Stops the currently running feature.
- **Exit**: Closes the application.

### 3. Quit the Application

You can stop any running feature and then exit the GUI.

---

## Troubleshooting

### Common Issues:

1. **"shape_predictor_68_face_landmarks.dat" Not Found**
   - Ensure the file is in the same directory as the scripts.

2. **Webcam Not Detected**
   - Check if another application is using the webcam.
   - Verify the webcam is connected and functional.

3. **Dependencies Not Installed**
   - Re-run `pip install -r requirements.txt`.

4. **Permission Denied**
   - Run the script with administrator privileges if required.

---

## Note

- This project is for demonstration purposes and may not be fully optimized for all environments.
- Ensure proper lighting for the webcam to detect head movements accurately.

