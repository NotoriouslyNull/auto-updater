#!/usr/bin/env python3

import subprocess
import json
import requests
import shutil
import socket

# Function to install pip if not installed
def install_pip():
    pip_installed = shutil.which("pip3") is not None
    if not pip_installed:
        print("pip3 is not installed. Installing pip3...")
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-pip"])
    else:
        print("pip3 is already installed.")

# Function to install required Python packages
def install_required_packages():
    try:
        import requests
    except ImportError:
        print("requests module not found. Installing requests...")
        subprocess.run(["pip3", "install", "requests"])
    else:
        print("requests module is already installed.")

# Update and upgrade packages
def update_server():
    update_command = ["sudo", "apt-get", "update"]
    update_result = subprocess.run(update_command, capture_output=True, text=True)

    upgrade_command = ["sudo", "apt-get", "upgrade", "-y"]
    upgrade_result = subprocess.run(upgrade_command, capture_output=True, text=True)

    return update_result.stdout + "\n" + upgrade_result.stdout

# Parse the output to get updated packages
def parse_update_output(output):
    lines = output.split('\n')
    updates = []
    for line in lines:
        if "Inst" in line:
            updates.append(line.strip())
    return updates

# Format the updates for Discord message
def format_updates_for_discord(hostname, updates):
    if not updates:
        return f"{hostname} was checked but no updates were installed."

    formatted_updates = f"{hostname} updated the following packages:\n"
    for update in updates:
        formatted_updates += f"- {update}\n"
    return formatted_updates

# Send the update notification to Discord
def send_discord_notification(webhook_url, message):
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response.status_code, response.text

def main():
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

    # Get the hostname of the server
    hostname = socket.gethostname()

    # Ensure pip is installed
    install_pip()

    # Ensure required packages are installed
    install_required_packages()

    # Perform the update and get the output
    update_output = update_server()

    # Parse the update output
    updates = parse_update_output(update_output)

    # Format the updates for Discord
    discord_message = format_updates_for_discord(hostname, updates)

    # Send the notification to Discord
    status_code, response_text = send_discord_notification(webhook_url, discord_message)
    if status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {status_code}, Response: {response_text}")

if __name__ == "__main__":
    main()
