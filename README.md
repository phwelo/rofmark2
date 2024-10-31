# Bookmark Manager with Rofi

This project is a Python-based tool that allows you to manage and open bookmarks in specific Firefox container profiles, using Rofi as a selection menu. The script supports configurable profiles, bookmark tracking, and the option to perform web searches for unmatched entries.

## Features

- **Bookmark Management**: Define bookmarks in a JSON file, organized by profiles.
- **Rofi Menu Interface**: Choose bookmarks or perform a web search through a customizable Rofi menu.
- **Firefox Container Support**: Open URLs in specific Firefox containers using the [open-url-in-container](https://github.com/honsiorovskyi/open-url-in-container) extension.
- **Selection Tracking**: Track and update the number of times each bookmark is selected.
- **Configurable Options**: Customize settings via `config.ini` for flexibility.

## Prerequisites

### 1. Firefox (modern version)
Ensure you have a recent version of Firefox with container support.

### 2. [open-url-in-container Extension](https://github.com/honsiorovskyi/open-url-in-container)
This Firefox extension allows URLs to be opened directly in specified Firefox containers. Install and configure containers to match your defined profiles.

### 3. Rofi
Rofi is required for displaying the interactive menu to select bookmarks. Install Rofi if not already available.

### 4. Python 3.x
The script requires Python 3 with the following libraries:
```bash
pip install configparser
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/bookmark_manager.git
   cd bookmark_manager
   ```

2. **Install Required Python Libraries**:
   ```bash
   pip install configparser
   ```

3. **Configure `config.ini`**:
   Customize `config.ini` in the same directory as the script. Use the template below to define settings and profiles.

## Configuration

The `config.ini` file allows easy customization of paths, profiles, and options.

### Example `config.ini`

```ini
[Settings]
BOOKMARKS_FILE = /home/yourusername/bookmarks/bookmarks.json
FIREFOX_EXECUTABLE = firefox
THEME_PATH = /home/yourusername/.config/rofi/launchers/type-6/style-ph.rasi
SEARCH_URL = https://www.google.com/search?q=
DEFAULT_SEARCH_PROFILE = Personal
DEFAULT_GOOGLE_URL = https://google.com
ROFI_CASE_INSENSITIVE = true
ROFI_MATCHING_MODE = fuzzy

[Profiles]
PROFILES = Personal, Work, Research
```

- **BOOKMARKS_FILE**: Path to the JSON file containing your bookmarks.
- **FIREFOX_EXECUTABLE**: Path or name of the Firefox executable.
- **THEME_PATH**: Rofi theme file path.
- **SEARCH_URL**: Base URL for web searches.
- **DEFAULT_SEARCH_PROFILE**: Profile to use by default when searching the web.
- **DEFAULT_GOOGLE_URL**: URL for the default Google search option.
- **ROFI_CASE_INSENSITIVE**: Enables case-insensitive matching.
- **ROFI_MATCHING_MODE**: Sets Rofi matching mode (`fuzzy`, `regex`, etc.).
- **PROFILES**: Comma-separated list of container profiles matching Firefox container names.

## Usage

1. **Define Bookmarks in JSON**:
   Create a `bookmarks.json` file containing your bookmarks. Here’s an example structure:

   ```json
   [
       {
           "Display Name": "Email",
           "URL": "https://mail.google.com",
           "Profile": "Personal",
           "Count": 0
       },
       {
           "Display Name": "Project Management",
           "URL": "https://projectmanagement.com",
           "Profile": "Work",
           "Count": 0
       }
   ]
   ```

2. **Run the Script**:
   ```bash
   ./bookmark_manager.py
   ```

3. **Select Bookmark or Search Option**:
   The Rofi menu will display available bookmarks and a default search option. Selecting a bookmark will open it in the specified Firefox container profile, and the `Count` will increment in the JSON file. If no bookmark matches, a web search will be performed using the query entered.

### Example JSON Structure

An example `bookmarks.json` file might look like this:

```json
[
    {
        "Display Name": "Calendar",
        "URL": "https://calendar.google.com",
        "Profile": "Personal",
        "Count": 1
    },
    {
        "Display Name": "Docs",
        "URL": "https://docs.example.com",
        "Profile": "Work",
        "Count": 0
    }
]
```

## Troubleshooting

1. **Firefox Profile Not Found**:
   Ensure profiles in `config.ini` match those defined in the Firefox extension.

2. **Missing `config.ini` or `bookmarks.json`**:
   Ensure both `config.ini` and `bookmarks.json` are in place and correctly referenced.

3. **Rofi Not Installed**:
   Rofi is required. Install Rofi to use the menu selection feature.

## License

This project is licensed under the MIT License.
