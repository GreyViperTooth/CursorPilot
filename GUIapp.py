import tkinter as tk
from tkinter import messagebox
import subprocess

# Global variable to store the running process
running_process = None

# Function to start the selected feature
# mode: "cursor" for cursor movement, "scroll_video" for scrolling and video control
def start_feature(mode):
    global running_process
    if running_process:
        # Warn if a feature is already running
        messagebox.showwarning("Warning", "Another feature is already running!")
        return

    # Determine which script to run based on the mode
    if mode == "cursor":
        script = "cursormove.py"  # Replace with the file name for Cursor Movement
    elif mode == "scroll_video":
        script = "scrollvid.py"  # Replace with the file name for Scroll & Video
    else:
        return

    # Start the script as a subprocess
    running_process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to stop the currently running feature
def stop_feature():
    global running_process
    if running_process:
        # Terminate the subprocess and reset the process variable
        running_process.terminate()
        running_process = None
        messagebox.showinfo("Info", "Feature stopped successfully.")
    else:
        # Warn if no feature is currently running
        messagebox.showwarning("Warning", "No feature is currently running!")

# Function to create the GUI application
def create_gui():
    # Create the main application window
    root = tk.Tk()
    root.title("CursorPilot")
    root.geometry("400x300")

    # Add title label to the window
    title_label = tk.Label(root, text="CursorPilot", font=("Arial", 16))
    title_label.pack(pady=20)

    # Button to start Cursor Movement feature
    btn_cursor = tk.Button(root, text="Cursor Movement", font=("Arial", 12), command=lambda: start_feature("cursor"))
    btn_cursor.pack(pady=10)

    # Button to start Scroll & Video Playback feature
    btn_scroll_video = tk.Button(root, text="Scroll & Video Playback", font=("Arial", 12),
                                 command=lambda: start_feature("scroll_video"))
    btn_scroll_video.pack(pady=10)

    # Button to stop the currently running feature
    btn_stop = tk.Button(root, text="Stop Feature", font=("Arial", 12), command=stop_feature)
    btn_stop.pack(pady=10)

    # Exit button to close the application
    btn_exit = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
    btn_exit.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

# Entry point of the application
if __name__ == "__main__":
    create_gui()
