#!/usr/bin/env python3
import json
import subprocess
import os
import configparser
import shlex
import shutil

# Load configuration from config.ini in the same directory as the script
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))
BOOKMARKS_FILE = config.get("Settings", "BOOKMARKS_FILE")
FIREFOX_EXECUTABLE = config.get("Settings", "FIREFOX_EXECUTABLE")
THEME_PATH = shlex.quote(os.path.expanduser(config.get("Settings", "THEME_PATH")))
SEARCH_URL = config.get("Settings", "SEARCH_URL")
PROFILES = [profile.strip() for profile in config.get("Profiles", "PROFILES").split(",")]

def validate_config():
    if not os.path.exists(BOOKMARKS_FILE):
        print(f"Error: Bookmarks file '{BOOKMARKS_FILE}' does not exist.")
    if not shutil.which(FIREFOX_EXECUTABLE):
        print(f"Error: Firefox executable '{FIREFOX_EXECUTABLE}' not found.")
    if not os.path.exists(THEME_PATH.strip("'")):
        print(f"Error: Rofi theme path '{THEME_PATH}' does not exist.")

# Load bookmarks from the JSON file
def load_bookmarks():
    if os.path.exists(BOOKMARKS_FILE):
        with open(BOOKMARKS_FILE, "r") as f:
            return json.load(f)
    else:
        return []  # If no file exists, return an empty list

# Save updated bookmarks to the JSON file
def save_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bookmarks, f, indent=4)

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

# Load Rofi customization options from config
def load_rofi_options():
    rofi_case_insensitive = config.getboolean("Settings", "ROFI_CASE_INSENSITIVE", fallback=True)
    rofi_matching_mode = config.get("Settings", "ROFI_MATCHING_MODE", fallback="fuzzy")

    rofi_options = ["-dmenu", "-p", "Select Bookmark", "-theme", THEME_PATH]
    if rofi_case_insensitive:
        rofi_options.append("-i")
    rofi_options.extend(["-matching", rofi_matching_mode])
    return rofi_options

# Prepare the choices list for the Rofi menu
def prepare_choices(bookmarks):
    choices = []
    for profile in PROFILES:
        choices.append(f"Google ({profile})")
    for bookmark in bookmarks:
        choices.append(f"{bookmark['Display Name']} ({bookmark['Profile']}) - {bookmark['Count']}")
    return choices

# Display Rofi menu with prepared options and choices
def display_rofi_menu(rofi_options, choices):
    choice = subprocess.run(
        ["rofi"] + rofi_options,
        input="\n".join(choices).encode(),
        stdout=subprocess.PIPE
    ).stdout.decode().strip()
    return choice

# Generate Rofi menu with bookmarks, using helper functions
def generate_rofi_menu(bookmarks):
    rofi_options = load_rofi_options()
    choices = prepare_choices(bookmarks)
    return display_rofi_menu(rofi_options, choices)

# Handle default Google choice for each profile
def handle_google_choice(choice):
    for profile in PROFILES:
        if choice.lower() == f"google ({profile})".lower():
            open_in_firefox("https://google.com", profile)
            return True
    return False

# Handle a selected bookmark, incrementing its count and saving updates
def handle_bookmark_choice(choice, bookmarks):
    for bookmark in bookmarks:
        bookmark_display = f"{bookmark['Display Name']} ({bookmark['Profile']}) - {bookmark['Count']}".lower()
        if choice.lower() == bookmark_display:
            bookmark['Count'] += 1  # Increment count
            save_bookmarks(bookmarks)  # Save updated count to JSON
            open_in_firefox(bookmark['URL'], bookmark['Profile'])
            return True
    return False

# Perform a web search if no matching bookmark or Google option is found
def perform_web_search(choice):
    search_query = choice.replace(" ", "+")  # Prepare the query for a URL
    search_url = f"{SEARCH_URL}{search_query}"
    print(f"No matching bookmark found. Searching the web for '{choice}'...")
    open_in_firefox(search_url, PROFILES[0])  # Default to the first profile for searches

# Main function
def main():
    bookmarks = load_bookmarks()
    validate_config()
    choice = generate_rofi_menu(bookmarks)
    
    if choice:
        if handle_google_choice(choice):
            return
        if handle_bookmark_choice(choice, bookmarks):
            return
        perform_web_search(choice)

if __name__ == "__main__":
    main()
