#!/usr/bin/env python3
import json
import subprocess
import os
import configparser
import shlex

# Determine the directory of the running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load configuration from config.ini in the script's directory
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, "config.ini"))

# Path to the bookmarks.json file
BOOKMARKS_FILE = config.get("Settings", "BOOKMARKS_FILE")

# Firefox executable path
FIREFOX_EXECUTABLE = config.get("Settings", "FIREFOX_EXECUTABLE")

# Theme path for rofi
THEME_PATH = shlex.quote(os.path.expanduser(config.get("Settings", "THEME_PATH")))


# List of profiles
PROFILES = [profile.strip() for profile in config.get("Profiles", "PROFILES").split(",")]

# Load bookmarks from the JSON file
def load_bookmarks():
    if os.path.exists(BOOKMARKS_FILE):
        with open(BOOKMARKS_FILE, "r") as f:
            return json.load(f)
    else:
        return []  # If no file exists, return an empty list

# Ensure the profile is valid
def is_valid_profile(profile):
    return profile in PROFILES

# Open the selected bookmark or default Google in the correct Firefox profile
def open_in_firefox(url, profile):
    if is_valid_profile(profile):
        container_url = f"ext+container:name={profile}&url={url}"
        subprocess.run([FIREFOX_EXECUTABLE, container_url])
    else:
        print(f"Profile '{profile}' is invalid.")

# Generate rofi menu with bookmarks, using a .rasi theme
def generate_rofi_menu(bookmarks):
    choices = []
    
    # Add default Google items for each profile
    for profile in PROFILES:
        choices.append(f"Google ({profile})")
    
    # Add bookmarks if any exist
    for bookmark in bookmarks:
        choices.append(f"{bookmark['Display Name']} ({bookmark['Profile']})")

    # Run rofi menu with fuzzy search and case-insensitivity
    choice = subprocess.run(
        ["rofi", "-dmenu", "-p", "Select Bookmark", "-theme", THEME_PATH, "-i", "-matching", "fuzzy"],
        input="\n".join(choices).encode(),
        stdout=subprocess.PIPE
    ).stdout.decode().strip()
    
    return choice


# Main function
def main():
    bookmarks = load_bookmarks()
    
    # Show the rofi menu
    choice = generate_rofi_menu(bookmarks)
    
    if choice:
        # Check if the choice is a Google default for any profile
        for profile in PROFILES:
            if choice.lower() == f"google ({profile})".lower():
                open_in_firefox("https://google.com", profile)
                return
        
        # Match against bookmarks
        for bookmark in bookmarks:
            bookmark_display = f"{bookmark['Display Name']} ({bookmark['Profile']})".lower()
            if choice.lower() == bookmark_display:
                open_in_firefox(bookmark['URL'], bookmark['Profile'])
                return

        # If no match is found, notify
        print("No matching bookmark found")

if __name__ == "__main__":
    main()
