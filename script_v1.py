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

# Define the robot's initial position and appearance
robot_x = 30
robot_y = 60
robot_size = 30

# Define the moose's initial position and appearance
moose_x = 200
moose_y = 60
moose_size = 40

# Define the robot's movement and animation
def draw_robot(draw, x, y, size, action):
    print(f"Drawing robot at ({x}, {y}) with action: {action}")
    # Draw the robot's head
    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)
    # Draw the robot's eyes
    draw.ellipse((x - size // 2, y - size // 2, x - size // 4, y - size // 4), fill=255)
    draw.ellipse((x + size // 4, y - size // 2, x + size // 2, y - size // 4), fill=255)
    # Draw the robot's mouth
    if action == "talk":
        draw.rectangle((x - size // 2, y + size // 2, x + size // 2, y + size), fill=0)
    else:
        draw.arc((x - size // 2, y + size // 4, x + size // 2, y + size), start=0, end=180, fill=0)

    # Draw the robot's body
    draw.rectangle((x - size, y + size, x + size, y + 2 * size), fill=0)
    # Draw the robot's arms
    if action == "dance":
        draw.line((x - size, y + size, x - 2 * size, y), fill=0, width=2)
        draw.line((x + size, y + size, x + 2 * size, y), fill=0, width=2)
    elif action == "fight":
        # Draw a slashing sword
        draw.line((x + size, y, x + 3 * size, y - size), fill=0, width=2)
    else:
        draw.line((x - size, y + size, x - 2 * size, y + size), fill=0, width=2)
        draw.line((x + size, y + size, x + 2 * size, y + size), fill=0, width=2)
    # Draw the robot's legs
    if action == "walk":
        draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill=0, width=2)
        draw.line((x + size // 2, y + 2 * size, x + size, y + 3 * size), fill=0, width=2)
    else:
        draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill=0, width=2)
        draw.line((x + size // 2, y + 2 * size, x + size // 2, y + 3 * size), fill=0, width=2)

# Define the moose's appearance
def draw_moose(draw, x, y, size):
    print(f"Drawing moose at ({x}, {y})")
    # Draw the moose's head
    draw.ellipse((x - size, y - size, x + size, y + size), fill=0)
    # Draw the moose's antlers
    draw.line((x - size, y - size, x - 2 * size, y - 2 * size), fill=0, width=2)
    draw.line((x + size, y - size, x + 2 * size, y - 2 * size), fill=0, width=2)
    # Draw the moose's eyes
    draw.ellipse((x - size // 2, y - size // 2, x - size // 4, y - size // 4), fill=255)
    draw.ellipse((x + size // 4, y - size // 2, x + size // 2, y - size // 4), fill=255)
    # Draw the moose's body
    draw.rectangle((x - size, y + size, x + size, y + 2 * size), fill=0)
    # Draw the moose's legs
    draw.line((x - size // 2, y + 2 * size, x - size // 2, y + 3 * size), fill=0, width=2)
    draw.line((x + size // 2, y + 2 * size, x + size // 2, y + 3 * size), fill=0, width=2)

# Define the phrases the robot can say
phrases = [
    "Jesus loves you!",
    "Your mom and dad love you!",
    "Watch out for moose!",
    "Chicken jockey!",
    "Shish-kabob!"
]

# Main loop
try:
    while True:
        print("Creating a new image...")
        # Create a new image with swapped dimensions for landscape mode
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        # Choose a random action for the robot
        action = random.choice(["walk", "dance", "fight", "talk"])
        print(f"Selected action: {action}")

        # Draw the robot
        draw_robot(draw, robot_y, robot_x, robot_size, action)

        # Draw the moose if the robot is fighting
        if action == "fight":
            draw_moose(draw, moose_y, moose_x, moose_size)

        # Display a random phrase if the robot is talking
        if action == "talk":
            phrase = random.choice(phrases)
            print(f"Displaying phrase: {phrase}")
            # Draw a dialogue box in the top right corner
            dialogue_box_x = epd.height - 110
            dialogue_box_y = 10
            draw.rectangle((dialogue_box_x, dialogue_box_y, dialogue_box_x + 100, dialogue_box_y + 40), fill=255, outline=0)
            # Wrap the text to fit in the dialogue box
            wrapped_text = textwrap.fill(phrase, width=12)
            draw.text((dialogue_box_x + 5, dialogue_box_y + 5), wrapped_text, fill=0)

        # Display the image on the e-Ink display
        print("Displaying image on e-Ink display...")
        epd.display(epd.getbuffer(image))
        print("Image displayed.")

        # Move the robot randomly
        if action == "walk":
            robot_x += random.choice([-5, 5])
        elif action == "dance":
            robot_x += random.choice([-10, 10])

        # Ensure the robot stays within the display bounds
        robot_x = max(robot_size, min(epd.height - robot_size, robot_x))
        robot_y = max(robot_size, min(epd.width - robot_size, robot_y))

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
