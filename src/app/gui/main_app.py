# main_app.py
import sys
import tkinter as tk

from src.app.gui.config_screen import ConfigScreen
from src.app.gui.main_screen import MainScreen
from src.app.utils.config import ConfigManager
from src.app.utils.exceptions import ConfigurationError, DatabaseError
from src.app.utils.logger import setup_logger
from src.app.utils.setup import check_initialization

logger = setup_logger()


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Africa Oncology Data Collection")
        self.geometry("800x600")
        self.config_manager = ConfigManager()

        # Placeholder for the current screen
        self.current_screen = None

        try:
            # Check if both config and database exist
            if check_initialization():
                # Both exist, proceed to main screen
                self.show_main_screen()
            else:
                # One or both missing, show config screen
                logger.info("Configuration or database missing. Showing config screen.")
                self.show_config_screen()
        except Exception as e:
            logger.warning(f"Initialization check failed: {e}")
            self.show_config_screen()

    def show_config_screen(self):
        """Display the configuration screen."""
        self.clear_screen()
        self.current_screen = ConfigScreen(self)
        self.current_screen.pack(expand=True, fill="both")

    def show_main_screen(self):
        """Display the main application screen."""
        self.clear_screen()
        self.current_screen = MainScreen(self)
        self.current_screen.pack(expand=True, fill="both")

    def clear_screen(self):
        """Destroy the current screen to transition to another."""
        if self.current_screen:
            self.current_screen.destroy()

    def run(self):
        try:
            self.mainloop()
        except ConfigurationError:
            logger.error("Configuration failed. Relaunching configuration screen.")
            self.show_config_screen()
        except DatabaseError:
            logger.error("Database initialization failed.")
            sys.exit(3)
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            sys.exit(1)
