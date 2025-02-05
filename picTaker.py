import cv2
import numpy as np
import time
import cv2
import time
from PIL import Image
import win32print
import win32ui
from PIL import ImageWin

import tkinter as tk
from tkinter import Label, Button, filedialog
import cv2
import time
from PIL import Image, ImageTk

# Function to capture photo from the camera
def capture_photo():
    # Clear the previous image from the preview
    blank_img = Image.new("RGB", (300, 300), "white")
    img_tk = ImageTk.PhotoImage(blank_img)
    preview_label.configure(image=img_tk)
    preview_label.image = img_tk


    cap = cv2.VideoCapture(0)  # Open the default camera (index 0)
    time.sleep(2)  # Wait for 2 seconds to allow the camera to focus
    ret, frame = cap.read()  # Capture a frame from the camera
    if ret:
        # Save the captured photo to a specified path
        photo_path = 'C:\\Users\\HP\\Desktop\\python-photos-app\\photo.jpg'
        cv2.imwrite(photo_path, frame)
        # Apply background to the captured photo
    else:
        print("Failed to capture image")  # Print an error message if capture fails
    cap.release()  # Release the camera
    return photo_path  # Return the path of the captured photo

# Function to apply a background to the captured photo
def apply_background(image_path, background_path):
    img = cv2.imread(image_path)  # Read the captured image
    bg = cv2.imread(background_path)  # Read the background image

    # Simulate segmentation by converting to HSV and creating a mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)  # Create mask for green color
    mask_inv = cv2.bitwise_not(mask)  # Invert the mask
    img_bg = cv2.bitwise_and(img, img, mask=mask_inv)  # Extract the foreground
    bg_fg = cv2.bitwise_and(bg, bg, mask=mask)  # Extract the background
    combined = cv2.add(img_bg, bg_fg)  # Combine foreground and background

    # Save the combined image to a specified path
    output_path = 'C:\\Users\\HP\\Desktop\\python-photos-app\\output.jpg'
    cv2.imwrite(output_path, combined)
    return output_path  # Return the path of the combined image

# Function to update the preview label with the captured image
def update_preview():
    photo_path = capture_photo()  # Capture the photo
    #uncomment this when you have green screen and background image
    # output_path = apply_background(photo_path, 'C:\\Users\\HP\\Desktop\\python-photos-app\\background.jpg')  # Apply background
    output_path = photo_path
    img = Image.open(output_path)  # Open the combined image
    img = img.resize((300, 300))  # Resize the image for preview
    img_tk = ImageTk.PhotoImage(img)  # Convert the image to a format suitable for Tkinter
    preview_label.configure(image=img_tk)  # Update the preview label with the image
    preview_label.image = img_tk  # Keep a reference to the image to prevent garbage collection

# Placeholder function for printing the image
def print_image():
    print("Print button clicked. Implement the print logic here.")

# def print_image(image_path):
#     hDC = win32ui.CreateDC()  # Create a device context object
#     hDC.CreatePrinterDC(win32print.GetDefaultPrinter())  # Set the default printer
#     bmp = Image.open(image_path)  # Open the image using PIL

#     # Set image size and position for printing
#     printable_area = hDC.GetDeviceCaps(8), hDC.GetDeviceCaps(10)  # Get printable area dimensions
#     bmp = bmp.resize(printable_area)  # Resize the image to fit the printable area
#     dib = ImageWin.Dib(bmp)  # Convert the image to a device-independent bitmap (DIB)
#     dib.draw(hDC.GetHandleOutput(), (0, 0, bmp.size[0], bmp.size[1]))  # Draw the DIB on the printer device context

#     hDC.EndPage()  # End the current page
#     hDC.EndDoc()  # End the print job
#     hDC.DeleteDC()  # Delete the device context

# Create the main window
root = tk.Tk()
root.title("Photo Capture and Print")  # Set the window title
root.geometry("400x500")  # Set the window size

# Create and place the Capture button
capture_button = Button(root, text="Capture", command=update_preview)
capture_button.pack(pady=10)
# Create and place the Print button
print_button = Button(root, text="Print", command=print_image)
print_button.pack(pady=10)

# Create a label to show the preview of the captured image
preview_label = Label(root)
preview_label.pack(pady=20)

# Run the main event loop
root.mainloop()
