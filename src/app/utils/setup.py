from src.app.utils.config import DATABASE_FILE, ConfigManager


def initialize_app():
    """Ensure the application is properly initialized."""
    initialize_settings()
    initialize_database()


def initialize_settings():
    """Ensure the settings file and directory exist."""
    config_manager = ConfigManager()
    if not config_manager.settings.get("db_path"):
        raise ValueError("Database path is missing in configuration.")


def initialize_database():
    """Ensure the database file exists and is initialized."""
    db_path = DATABASE_FILE
    if not DATABASE_FILE.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")
