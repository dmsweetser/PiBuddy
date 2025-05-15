import os
import epd
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import random
import textwrap

# Initialize the e-Ink display
print("Initializing e-Ink display...")
epd = epd.EPD()
epd.init()
epd.Clear(0xFF)
print("e-Ink display initialized and cleared.")

# Define the cat's initial position and appearance
cat_x = 30
cat_y = 60
cat_size = 30

# Define the ground's initial position
ground_y = epd.width - 10

# Define the objects' initial positions and appearances
mouse_x = 200
mouse_y = 60
mouse_size = 10

rock_x = 200
rock_y = 60
rock_size = 15

dog_x = 200
dog_y = 60
dog_size = 20

# Define the cat's movement and animation
def draw_cat(draw, x, y, size, action):
    print(f"Drawing cat at ({x}, {y}) with action: {action}")
    # Draw the cat's head
    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)
    # Draw the cat's eyes
    draw.ellipse((x - size // 2, y - size // 2, x - size // 4, y - size // 4), fill=255)
    draw.ellipse((x + size // 4, y - size // 2, x + size // 2, y - size // 4), fill=255)
    # Draw the cat's mouth
    if action == "talk":
        draw.rectangle((x - size // 2, y + size // 2, x + size // 2, y + size), fill=0)
    else:
        draw.arc((x - size // 2, y + size // 4, x + size // 2, y + size), start=0, end=180, fill=0)

    # Draw the cat's body
    draw.rectangle((x - size, y + size, x + size, y + 2 * size), fill=0)
    # Draw the cat's legs
    if action == "walk":
        draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill=0, width=2)
        draw.line((x + size // 2, y + 2 * size, x + size, y + 3 * size), fill=0, width=2)
    else:
        draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill=0, width=2)
        draw.line((x + size // 2, y + 2 * size, x + size // 2, y + 3 * size), fill=0, width=2)

# Define the mouse's appearance
def draw_mouse(draw, x, y, size):
    print(f"Drawing mouse at ({x}, {y})")
    # Draw the mouse's body
    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)
    # Draw the mouse's eyes
    draw.ellipse((x - size // 2, y - size // 2, x - size // 4, y - size // 4), fill=255)
    draw.ellipse((x + size // 4, y - size // 2, x + size // 2, y - size // 4), fill=255)
    # Draw the mouse's tail
    draw.line((x + size, y, x + 2 * size, y), fill=0, width=1)

# Define the rock's appearance
def draw_rock(draw, x, y, size):
    print(f"Drawing rock at ({x}, {y})")
    # Draw the rock
    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)

# Define the dog's appearance
def draw_dog(draw, x, y, size):
    print(f"Drawing dog at ({x}, {y})")
    # Draw the dog's head
    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)
    # Draw the dog's eyes
    draw.ellipse((x - size // 2, y - size // 2, x - size // 4, y - size // 4), fill=255)
    draw.ellipse((x + size // 4, y - size // 2, x + size // 2, y - size // 4), fill=255)
    # Draw the dog's body
    draw.rectangle((x - size, y + size, x + size, y + 2 * size), fill=0)
    # Draw the dog's legs
    draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill=0, width=2)
    draw.line((x + size // 2, y + 2 * size, x + size // 2, y + 3 * size), fill=0, width=2)

# Define the ground's appearance
def draw_ground(draw, y):
    print(f"Drawing ground at y={y}")
    # Draw the ground
    draw.rectangle((0, y, epd.height, y + 10), fill=0)

# Main loop
try:
    while True:
        print("Creating a new image...")
        # Create a new image with swapped dimensions for landscape mode
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Choose a random action for the cat
        action = random.choice(["walk", "talk"])
        print(f"Selected action: {action}")

        # Draw the cat
        draw_cat(draw, cat_y, cat_x, cat_size, action)

        # Draw the ground
        draw_ground(draw, ground_y)

        # Randomly decide whether to draw an object
        object_to_draw = random.choice([None, "mouse", "rock", "dog"])
        if object_to_draw == "mouse":
            draw_mouse(draw, mouse_y, mouse_x, mouse_size)
        elif object_to_draw == "rock":
            draw_rock(draw, rock_y, rock_x, rock_size)
        elif object_to_draw == "dog":
            draw_dog(draw, dog_y, dog_x, dog_size)

        # Display the image on the e-Ink display
        print("Displaying image on e-Ink display...")
        epd.display(epd.getbuffer(image))
        print("Image displayed.")

        # Move the cat randomly
        if action == "walk":
            cat_x += random.choice([-5, 5])

        # Ensure the cat stays within the display bounds
        cat_x = max(cat_size, min(epd.height - cat_size, cat_x))
        cat_y = max(cat_size, min(epd.width - cat_size, cat_y))

        # Wait for a longer period before updating the display again
        if action == "talk":
            time.sleep(5)  # Longer delay for talking
        else:
            time.sleep(1)  # Shorter delay for other actions

except KeyboardInterrupt:
    print("Keyboard interrupt detected. Cleaning up...")
    # Clean up the e-Ink display
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
    epd.epdconfig.module_exit(cleanup=True)
    exit()
