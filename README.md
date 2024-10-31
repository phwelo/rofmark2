# WLED Bookmark Manager

This project is a Python-based tool for managing WLED bookmarks across different Firefox profiles. It leverages the [open-url-in-container](https://github.com/honsiorovskyi/open-url-in-container) Firefox extension to open URLs in specific Firefox containers. Bookmarks are defined in a JSON file and accessed via a Rofi menu with container-based handling.

## Prerequisites

### 1. Firefox (modern version)
Ensure you have a recent version of Firefox installed, as this script depends on container features introduced in newer versions.

### 2. [open-url-in-container Extension](https://github.com/honsiorovskyi/open-url-in-container)
This Firefox extension allows URLs to be opened directly in specified Firefox containers. Install this extension and configure containers to match the profiles defined in your configuration.

### 3. Python 3.x
This script is written in Python 3 and requires several Python libraries.

### 4. Rofi
Rofi is required for displaying the interactive menu to select bookmarks. Make sure Rofi is installed if you plan to use this feature.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/wled_scanner.git
   cd wled_scanner
   ```

2. **Install Required Python Libraries**:
   ```bash
   pip install configparser
   ```

3. **Download and Configure `config.ini`**:
   Customize `config.ini` in the same directory as the script, following the example below.

## Configuration

The `config.ini` file allows for easy customization of settings, including the bookmarks file path, Firefox executable, Rofi theme, and available profiles. Place this file in the same directory as the script.

### Example `config.ini`

```ini
[Settings]
BOOKMARKS_FILE = /home/yourusername/bookmarks/bookmarks.json
FIREFOX_EXECUTABLE = firefox
THEME_PATH = /home/yourusername/.config/rofi/launchers/type-6/style-ph.rasi

[Profiles]
PROFILES = Personal, Work, Admin, Research
```

- **BOOKMARKS_FILE**: Path to the JSON file containing your bookmarks.
- **FIREFOX_EXECUTABLE**: Path or name of the Firefox executable.
- **THEME_PATH**: Rofi theme file path.
- **PROFILES**: Comma-separated list of container profile names to match your Firefox container setup.

## Usage

1. **Prepare Bookmarks File**:
   Ensure that `bookmarks.json` exists and contains your bookmarks in the following format:

   ```json
   [
       {
           "Display Name": "Example Bookmark",
           "URL": "https://example.com",
           "Profile": "Personal",
           "Count": 0
       },
       {
           "Display Name": "Another Bookmark",
           "URL": "https://anotherexample.com",
           "Profile": "Work",
           "Count": 1
       }
   ]
   ```

2. **Run the Script**:
   ```bash
   ./bookmark_manager.py
   ```

3. **Select a Bookmark or Default Option**:
   The script will display a Rofi menu listing bookmarks and a default option for Google in each profile. Select an option to open it in the associated Firefox container.

### Using with Rofi

- The script generates a menu via Rofi with a specified theme. You can modify the theme by updating the `THEME_PATH` setting in `config.ini`.
- The menu supports fuzzy matching and is case-insensitive for convenience.

## Example JSON Structure

An example `bookmarks.json` file might look like this:

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
        "URL": "https://project.management.com",
        "Profile": "Work",
        "Count": 1
    }
]
```

## Troubleshooting

1. **Firefox Profile Not Found**:
   Make sure that the profiles in `config.ini` match the containers configured in your Firefox extension.

2. **Missing `config.ini` or `bookmarks.json`**:
   Ensure both `config.ini` and `bookmarks.json` are in place and correctly referenced in your configuration.

3. **Rofi Not Installed**:
   Rofi is required for this script to function. Make sure it is installed.

## License

This project is licensed under the MIT License.
