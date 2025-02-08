import cv2
import numpy as np

def apply_background(image_path, background_path):
    img = cv2.imread(image_path)  # Read the captured image
    bg = cv2.imread(background_path)  # Read the background image

    # Resize background to match the captured image dimensions
    bg = cv2.resize(bg, (img.shape[1], img.shape[0]))

    # Simulate segmentation by converting to HSV and creating a mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)  # Create mask for green color
    mask_inv = cv2.bitwise_not(mask)  # Invert the mask
    img_bg = cv2.bitwise_and(img, img, mask=mask_inv)  # Extract the foreground
    bg_fg = cv2.bitwise_and(bg, bg, mask=mask)  # Extract the background
    combined = cv2.add(img_bg, bg_fg)  # Combine foreground and background

    # Save the combined image to a specified path
    output_path = 'C:\\Users\\HP\\Desktop\\python-photos-app\\output pics\\output.jpg'
    cv2.imwrite(output_path, combined)
    return output_path  # Return the path of the combined image

apply_background("greenscreenpic2.jpg","greenscreenbg.jpg")

