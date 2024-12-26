import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".africa_oncology_settings.json"


class ConfigManager:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        """Load the settings from a file."""
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        else:
            return self.create_default_settings()

    def save_settings(self):
        """Save the current settings to a file."""
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def create_default_settings(self):
        """Create and save a default settings file."""
        default_settings = {"db_path": r"\\shared\WindowsDrive\path\to\database.sqlite"}
        with open(SETTINGS_FILE, "w") as file:
            json.dump(default_settings, file, indent=4)
        return default_settings
