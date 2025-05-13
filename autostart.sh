#!/bin/bash

# Define paths
SCRIPT_DIR="~/PiBuddy"
RUN_SCRIPT_PATH="$SCRIPT_DIR/run.sh"
SERVICE_NAME="robot"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

# Ensure the script is executable
chmod +x "$RUN_SCRIPT_PATH"

# Create the systemd service file
cat <<EOF | sudo tee "$SERVICE_FILE"
[Unit]
Description=Robot Script
After=multi-user.target

[Service]
Type=simple
ExecStart=/bin/bash $RUN_SCRIPT_PATH
WorkingDirectory=$SCRIPT_DIR
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable "$SERVICE_NAME"

# Start the service immediately
sudo systemctl start "$SERVICE_NAME"

# Check the status of the service
sudo systemctl status "$SERVICE_NAME"
