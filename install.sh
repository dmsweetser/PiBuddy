#!/bin/bash

# Update package list and install prerequisites
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-venv

# Create a virtual environment
python3.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set the script to run on machine startup
echo "@reboot /bin/bash $(pwd)/run.sh" | crontab -

echo "Setup complete."
