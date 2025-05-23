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

# Define Hobbes' initial position and appearance
hobbes_x = 30
hobbes_y = 60
hobbes_size = 30

# Define the ground's initial position
ground_y = epd.width - 10

# Define the objects' initial positions and appearances
bird_x = 200
bird_y = 60
bird_size = 10

fishbowl_x = 200
fishbowl_y = 60
fishbowl_size = 15

butterfly_x = 200
butterfly_y = 60
butterfly_size = 10

# Define Hobbes' appearance using anti-aliasing
def draw_hobbes(draw, x, y, size, action):
    print(f"Drawing Hobbes at ({x}, {y}) with action: {action}")

    # Draw Hobbes' head with anti-aliasing
    draw.ellipse((x - size, y - size, x + size, y + size), fill='white', outline='black')

    # Draw Hobbes' ears with anti-aliasing
    draw.polygon([(x - size, y - size), (x - size - 10, y - size - 10), (x - size, y - size - 20)], fill='white', outline='black')
    draw.polygon([(x + size, y - size), (x + size + 10, y - size - 10), (x + size, y - size - 20)], fill='white', outline='black')

    # Draw Hobbes' eyes with anti-aliasing
    draw.ellipse((x - size // 2, y - size // 2, x - size // 4, y - size // 4), fill='black')
    draw.ellipse((x + size // 4, y - size // 2, x + size // 2, y - size // 4), fill='black')

    # Draw Hobbes' nose with anti-aliasing
    draw.ellipse((x - 5, y + 5, x + 5, y + 15), fill='black')

    # Draw Hobbes' mouth with anti-aliasing
    if action == "meow":
        draw.arc((x - size // 2, y + size // 4, x + size // 2, y + size), start=0, end=180, fill='black')
    else:
        draw.line((x - size // 4, y + size // 2, x + size // 4, y + size // 2), fill='black', width=2)

    # Draw Hobbes' stripes with anti-aliasing
    stripe_width = 3
    for i in range(-size, size, stripe_width * 2):
        draw.line((x + i, y - size, x + i + stripe_width, y + size), fill='black', width=stripe_width)

    # Draw Hobbes' body with anti-aliasing
    draw.rectangle((x - size, y + size, x + size, y + 2 * size), fill='white', outline='black')

    # Draw Hobbes' legs with anti-aliasing
    if action == "walk":
        draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill='black', width=2)
        draw.line((x + size // 2, y + 2 * size, x + size, y + 3 * size), fill='black', width=2)
    else:
        draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill='black', width=2)
        draw.line((x + size // 2, y + 2 * size, x + size // 2, y + 3 * size), fill='black', width=2)

# Define the bird's appearance
def draw_bird(draw, x, y, size):
    print(f"Drawing bird at ({x}, {y})")
    # Draw the bird's body
    draw.ellipse((x - size, y - size, x + size, y + size), fill='black')
    # Draw the bird's beak
    draw.polygon([(x + size, y), (x + size + 10, y - 5), (x + size + 10, y + 5)], fill='black')
    # Draw the bird's wing
    draw.ellipse((x - size // 2, y - size // 2, x + size // 2, y + size // 2), fill='black')

# Define the fishbowl's appearance
def draw_fishbowl(draw, x, y, size):
    print(f"Drawing fishbowl at ({x}, {y})")
    # Draw the fishbowl
    draw.ellipse((x - size, y - size, x + size, y + size), fill='black')
    # Draw the fish inside the bowl
    draw.ellipse((x - size // 2, y - size // 2, x + size // 2, y + size // 2), fill='white')

# Define the butterfly's appearance
def draw_butterfly(draw, x, y, size):
    print(f"Drawing butterfly at ({x}, {y})")
    # Draw the butterfly's body
    draw.ellipse((x - size // 2, y - size // 2, x + size // 2, y + size // 2), fill='black')
    # Draw the butterfly's wings
    draw.ellipse((x - size, y - size, x, y), fill='black')
    draw.ellipse((x, y - size, x + size, y), fill='black')
    draw.ellipse((x - size, y, x, y + size), fill='black')
    draw.ellipse((x, y, x + size, y + size), fill='black')

# Define the ground's appearance
def draw_ground(draw, y):
    print(f"Drawing ground at y={y}")
    # Draw the ground
    draw.rectangle((0, y, epd.height, y + 10), fill='black')

# Main loop
try:
    while True:
        print("Creating a new image...")
        # Create a new image with swapped dimensions for landscape mode
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Choose a random action for Hobbes
        action = random.choice(["walk", "meow", "observe"])
        print(f"Selected action: {action}")

        # Draw Hobbes
        draw_hobbes(draw, hobbes_y, hobbes_x, hobbes_size, action)

        # Draw the ground
        draw_ground(draw, ground_y)

        # Randomly decide whether to draw an object
        object_to_draw = random.choice([None, "bird", "fishbowl", "butterfly"])
        if object_to_draw == "bird":
            draw_bird(draw, bird_y, bird_x, bird_size)
            # Check for interaction with Hobbes
            if abs(hobbes_x - bird_x) < hobbes_size + bird_size:
                action = "meow"
                draw_hobbes(draw, hobbes_y, hobbes_x, hobbes_size, action)
        elif object_to_draw == "fishbowl":
            draw_fishbowl(draw, fishbowl_y, fishbowl_x, fishbowl_size)
            # Check for interaction with Hobbes
            if abs(hobbes_x - fishbowl_x) < hobbes_size + fishbowl_size:
                action = "observe"
                draw_hobbes(draw, hobbes_y, hobbes_x, hobbes_size, action)
        elif object_to_draw == "butterfly":
            draw_butterfly(draw, butterfly_y, butterfly_x, butterfly_size)
            # Check for interaction with Hobbes
            if abs(hobbes_x - butterfly_x) < hobbes_size + butterfly_size:
                action = "walk"
                draw_hobbes(draw, hobbes_y, hobbes_x, hobbes_size, action)

        # Display the image on the e-Ink display
        print("Displaying image on e-Ink display...")
        epd.display(epd.getbuffer(image))
        print("Image displayed.")

        # Move Hobbes randomly
        if action == "walk":
            hobbes_x += random.choice([-5, 5])  # Smaller leaps for smoother movement

        # Ensure Hobbes stays within the display bounds
        hobbes_x = max(hobbes_size, min(epd.height - hobbes_size, hobbes_x))

        # Wait for a longer period before updating the display again
        if action == "meow":
            time.sleep(5)  # Longer delay for meowing
        elif action == "observe":
            time.sleep(3)  # Medium delay for observing
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
