import json
from pathlib import Path

from src.app.utils.exceptions import ConfigurationError, DatabaseError

# Define the application directory in the user's home directory
APP_DIR = Path.home() / "africa_oncology_settings"
SETTINGS_FILE = APP_DIR / "settings.json"
DATABASE_FILE = APP_DIR / "database.sqlite"


class ConfigManager:
    def __init__(self):
        # Ensure the application directory exists
        self.create_app_directory()
        # Initialize settings
        self.settings = self.load_settings()

    def create_app_directory(self):
        """Ensure the application directory exists."""
        APP_DIR.mkdir(exist_ok=True)

    def load_settings(self):
        """Load the settings from the settings file."""
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                # If file is invalid or corrupt, fall back to default settings
                return self.create_default_settings()
        else:
            return self.create_default_settings()

    def save_settings(self):
        """Save the current settings to the settings file."""
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def create_default_settings(self):
        """Create and return default settings."""
        default_settings = {"db_path": str(DATABASE_FILE)}
        self.settings = default_settings  # Ensure self.settings is initialized
        self.save_settings()  # Save default settings to file
        return default_settings


def initialize_settings():
    """Ensure the settings file and directory exist."""
    config_manager = ConfigManager()
    if not config_manager.settings.get("db_path"):
        raise ConfigurationError("Database path is missing in configuration.")


def initialize_database():
    """Ensure the database file exists and is initialized."""
    if not DATABASE_FILE.exists():
        raise DatabaseError(f"Database file not found: {DATABASE_FILE}")
