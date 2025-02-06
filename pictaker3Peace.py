import cv2
import numpy as np
import mediapipe as mp

import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Global flag to control the live preview
live_preview_running = True
captured_photo_path = 'C:\\Users\\HP\\Desktop\\python-photos-app\\photo.jpg'

# Function to capture photo from the camera
def capture_photo():
    ret, frame = cap.read()  # Capture a frame from the camera
    if ret:
        # Save the captured photo to a specified path
        cv2.imwrite(captured_photo_path, frame)
    else:
        print("Failed to capture image")  # Print an error message if capture fails
    return captured_photo_path  # Return the path of the captured photo

# Function to update the preview label with the captured image
def update_preview():
    global live_preview_running
    live_preview_running = False  # Stop the live preview
    photo_path = capture_photo()  # Capture the photo
    img = Image.open(photo_path)  # Open the captured image
    img = img.resize((300, 300))  # Resize the image for preview
    img_tk = ImageTk.PhotoImage(img)  # Convert the image to a format suitable for Tkinter
    live_preview_label.configure(image=img_tk)  # Update the preview label with the image
    live_preview_label.image = img_tk  # Keep a reference to the image to prevent garbage collection

# Function to restart the live preview
def restart_live_preview():
    global live_preview_running
    live_preview_running = True
    update_live_preview()

# Function to save the captured image
def save_image():
    print(f"Image already saved at {captured_photo_path}")

# Function to check if the peace sign gesture is shown
def is_peace_sign(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

    if (index_tip < thumb_tip and middle_tip < thumb_tip) and (ring_tip > index_tip and pinky_tip > middle_tip):
        return True
    return False

# Function to update the live preview
def update_live_preview():
    global live_preview_running
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Check if any hand is detected and if it shows the peace sign
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if is_peace_sign(hand_landmarks):
                    print("Peace sign detected. Showing final frame...")
                    live_preview_running = False  # Stop the live preview
                    # Show final frame and wait before capturing the photo
                    img = Image.fromarray(frame_rgb)
                    img = img.resize((300, 300))
                    img_tk = ImageTk.PhotoImage(img)
                    live_preview_label.configure(image=img_tk)
                    live_preview_label.image = img_tk
                    root.after(1000, update_preview)  # Delay before capturing the photo
                    return

        img = Image.fromarray(frame_rgb)
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        live_preview_label.configure(image=img_tk)
        live_preview_label.image = img_tk

    if live_preview_running:
        live_preview_label.after(10, update_live_preview)
# Create the main window
root = tk.Tk()
root.title("Photo Capture and Print")  # Set the window title
root.geometry("400x500")  # Set the window size

# Create and place the Capture button
capture_button = Button(root, text="Capture", command=restart_live_preview)
capture_button.pack(pady=10)
# Create and place the Print button
print_button = Button(root, text="Print", command=save_image)
print_button.pack(pady=10)

# Create a label to show the live camera feed and captured image
live_preview_label = Label(root)
live_preview_label.pack(pady=20)

cap = cv2.VideoCapture(0)  # Open the default camera

update_live_preview()  # Start the live preview

# Run the main event loop
root.mainloop()
