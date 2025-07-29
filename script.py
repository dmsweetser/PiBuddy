import os
import epd
import time
from PIL import Image, ImageDraw
import traceback
import random

# Initialize the e-Ink display
print("Initializing e-Ink display...")
epd = epd.EPD()
epd.init()
epd.Clear(0xFF)
print("e-Ink display initialized and cleared.")

# Define the face's initial position and size
face_x = epd.width // 2
face_y = epd.height // 2
face_size = 50

# Define the ground's initial position
ground_y = epd.width - 10

# Define the text's initial position
text_x = 10
text_y = 10

def draw_face(draw, x, y, size, action):
    print(f"Drawing face at ({x}, {y}) with action: {action}")

    # Draw the face outline
    draw.ellipse((x - size, y - size, x + size, y + size), fill='white', outline='black')

    # Draw the eyes
    eye_size = size // 4
    left_eye_x = x - size // 2
    right_eye_x = x + size // 2

    if action == "happy":
        # Draw happy eyes
        draw.ellipse((left_eye_x - eye_size, y - size // 2 - eye_size, left_eye_x + eye_size, y - size // 2 + eye_size), fill='black')
        draw.ellipse((right_eye_x - eye_size, y - size // 2 - eye_size, right_eye_x + eye_size, y - size // 2 + eye_size), fill='black')
    elif action == "sad":
        # Draw sad eyes
        draw.arc((left_eye_x - eye_size, y - size // 2 - eye_size, left_eye_x + eye_size, y - size // 2 + eye_size), start=0, end=180, fill='black')
        draw.arc((right_eye_x - eye_size, y - size // 2 - eye_size, right_eye_x + eye_size, y - size // 2 + eye_size), start=0, end=180, fill='black')
    else:
        # Draw neutral eyes
        draw.ellipse((left_eye_x - eye_size, y - size // 2 - eye_size, left_eye_x + eye_size, y - size // 2 + eye_size), fill='black')
        draw.ellipse((right_eye_x - eye_size, y - size // 2 - eye_size, right_eye_x + eye_size, y - size // 2 + eye_size), fill='black')

    # Draw the eyebrows
    eyebrow_length = size // 2
    left_eyebrow_y = y - size // 2 - eye_size - 5
    right_eyebrow_y = y - size // 2 - eye_size - 5

    if action == "happy":
        # Draw happy eyebrows
        draw.line((left_eye_x - eyebrow_length, left_eyebrow_y, left_eye_x + eyebrow_length, left_eyebrow_y - 10), fill='black', width=2)
        draw.line((right_eye_x - eyebrow_length, right_eyebrow_y, right_eye_x + eyebrow_length, right_eyebrow_y - 10), fill='black', width=2)
    elif action == "sad":
        # Draw sad eyebrows
        draw.line((left_eye_x - eyebrow_length, left_eyebrow_y + 10, left_eye_x + eyebrow_length, left_eyebrow_y), fill='black', width=2)
        draw.line((right_eye_x - eyebrow_length, right_eyebrow_y + 10, right_eye_x + eyebrow_length, right_eyebrow_y), fill='black', width=2)
    else:
        # Draw neutral eyebrows
        draw.line((left_eye_x - eyebrow_length, left_eyebrow_y, left_eye_x + eyebrow_length, left_eyebrow_y), fill='black', width=2)
        draw.line((right_eye_x - eyebrow_length, right_eyebrow_y, right_eye_x + eyebrow_length, right_eyebrow_y), fill='black', width=2)

    # Draw the mouth
    if action == "happy":
        # Draw a large smile with rounded teeth
        draw.arc((x - size // 2, y + size // 4, x + size // 2, y + 3 * size // 4), start=0, end=180, fill='black')
        tooth_size = size // 6
        for i in range(-size // 2 + tooth_size, size // 2, tooth_size * 2):
            draw.rectangle((x + i - tooth_size // 2, y + size // 2, x + i + tooth_size // 2, y + 3 * size // 4), fill='white', outline='black')
    elif action == "sad":
        # Draw a frown
        draw.arc((x - size // 2, y + size // 2, x + size // 2, y + 3 * size // 2), start=180, end=360, fill='black')
    else:
        # Draw a neutral mouth
        draw.line((x - size // 4, y + size // 2, x + size // 4, y + size // 2), fill='black', width=2)

def draw_ground(draw, y):
    print(f"Drawing ground at y={y}")
    # Draw the ground
    draw.rectangle((0, y, epd.height, y + 10), fill='black')

def draw_text(draw, text, x, y):
    print(f"Drawing text: {text} at ({x}, {y})")
    draw.text((x, y), text, fill='black')

try:
    while True:
        print("Creating a new image...")
        # Create a new image with swapped dimensions for landscape mode
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Choose a random action for the face
        action = random.choice(["happy", "sad", "neutral"])
        print(f"Selected action: {action}")

        # Draw the face
        draw_face(draw, face_y, face_x, face_size, action)

        # Draw the ground
        draw_ground(draw, ground_y)

        # Choose a random phrase to display
        phrases = ["Hello!", "How are you?", "Have a nice day!", "Smile!", "Stay happy!"]
        phrase = random.choice(phrases)
        print(f"Selected phrase: {phrase}")

        # Draw the text
        draw_text(draw, phrase, text_x, text_y)

        # Display the image on the e-Ink display
        print("Displaying image on e-Ink display...")
        epd.display(epd.getbuffer(image))
        print("Image displayed.")

        # Wait for a period before updating the display again
        time.sleep(3)

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Cleaning up...")
    # Clean up the e-Ink display
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
    exit()
