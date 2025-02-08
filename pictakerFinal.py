# import cv2
# import time
# import threading

# # Initialize the webcam for video capture. The argument '0' specifies the default camera.
# imgcapture = cv2.VideoCapture(0)
# countdown_text = ""
# capturing = False

# def countdown(n):
#     global countdown_text, capturing
#     while n > 0:
#         countdown_text = str(n)
#         time.sleep(1)
#         n -= 1
#     countdown_text = ""
#     capturing = True

# result = True

# while result:
#     ret, frame = imgcapture.read()  # Capture a frame from the webcam

#     # Add countdown text to the frame if available
#     if countdown_text:
#         frame = cv2.putText(frame, countdown_text, (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 255, 0), 4, cv2.LINE_AA)

#     cv2.imshow('Webcam Preview', frame)  # Show the live webcam preview

#     if capturing:
#         cv2.imwrite("test.jpeg", frame)
#         print("Image captured...")
#         capturing = False
#         result = False  # Exit the loop after capturing the image

#     # Check if the 'c' key is pressed to start the countdown
#     if cv2.waitKey(1) & 0xFF == ord('c'):
#         countdown_thread = threading.Thread(target=countdown, args=(3,))
#         countdown_thread.start()

# imgcapture.release()  # Release the webcam resource
# cv2.destroyAllWindows()  # Close all OpenCV windows


import cv2
import time
import threading
import tkinter as tk
from tkinter import Button
from PIL import Image, ImageTk

# Initialize the webcam for video capture. The argument '0' specifies the default camera.
imgcapture = cv2.VideoCapture(0)
countdown_text = ""
capturing = False
result = True
frame_rgb = None

def countdown(n):
    global countdown_text, capturing
    while n > 0:
        countdown_text = str(n)
        time.sleep(1)
        n -= 1
    countdown_text = ""
    capturing = True

def print_image():
    print("sent to print")

def retake_image():
    global capturing, result
    capturing = False
    result = True
    btn_print.pack_forget()
    btn_retake.pack_forget()
    btn_capture.pack(side=tk.BOTTOM, pady=20)  # Show the Capture button again
    show_frame()

def show_frame():
    global countdown_text, capturing, result, frame_rgb
    ret, frame = imgcapture.read()  # Capture a frame from the webcam

    if countdown_text:
        frame = cv2.putText(frame, countdown_text, (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 255, 0), 4, cv2.LINE_AA)

    # Resize the frame to cover 90% of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    frame = cv2.resize(frame, (int(screen_width * 0.9), int(screen_height * 0.9)))

    # Convert the frame to PIL format for Tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    
    # Show the frame in the Tkinter window
    lbl_video.imgtk = imgtk
    lbl_video.configure(image=imgtk)

    if capturing:
        # Capture a new frame without the countdown text
        frame_rgb = cv2.cvtColor(imgcapture.read()[1], cv2.COLOR_BGR2RGB)
        cv2.imwrite("test.jpeg", cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
        print("Image captured...")
        capturing = False
        # Resize the captured frame to make it bigger
        frame_rgb = cv2.resize(frame_rgb, (int(screen_width * 0.8), int(screen_height * 0.8)))
        # Show the captured frame
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        # Hide the Capture button and show Print and Retake buttons
        btn_capture.pack_forget()
        btn_print.pack(side=tk.LEFT, padx=10, pady=10)
        btn_retake.pack(side=tk.RIGHT, padx=10, pady=10)
    else:
        # Continue showing frames if not capturing
        if result:
            lbl_video.after(10, show_frame)

def capture_image():
    countdown_thread = threading.Thread(target=countdown, args=(3,))
    countdown_thread.start()

def exit_app():
    root.quit()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Webcam Preview")
root.attributes('-fullscreen', True)  # Set the window to fullscreen
root.configure(bg='#FFC0CB')  # Set background color to light pink
lbl_video = tk.Label(root, bg='#FFC0CB')
lbl_video.pack(expand=True, fill=tk.BOTH)

# Create Capture, Print, Retake, and Exit buttons with appropriate styles
btn_capture = Button(root, text="Capture", command=capture_image, font=("Helvetica", 24), padx=20, pady=10, bg='#008000', fg='#FFFFFF')
btn_print = Button(root, text="Print", command=print_image, font=("Helvetica", 24), padx=20, pady=10, bg='#8B0000', fg='#FFFFFF')
btn_retake = Button(root, text="Retake", command=retake_image, font=("Helvetica", 24), padx=20, pady=10, bg='#8B0000', fg='#FFFFFF')
btn_exit = Button(root, text="X", command=exit_app, font=("Helvetica", 18), bg='#FF0000', fg='#FFFFFF')

# Position the Capture button at the bottom center
btn_capture.pack(side=tk.BOTTOM, pady=20)
# Hide the Print and Retake buttons initially
btn_print.pack_forget()
btn_retake.pack_forget()
# Position the Exit button in the top right corner
btn_exit.place(x=root.winfo_screenwidth()-50, y=10)

# Start showing the webcam preview
show_frame()

# Start the Tkinter event loop
root.mainloop()

# Release the webcam resource and destroy the OpenCV windows
imgcapture.release()
cv2.destroyAllWindows()
