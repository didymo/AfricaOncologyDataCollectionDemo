import tkinter as tk

from src.app.gui.config_screen import ConfigScreen
from src.app.gui.main_screen import MainScreen
from src.app.utils.config import ConfigManager
from src.app.utils.logger import setup_logger
from src.app.utils.setup import initialize_app

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
            initialize_app()  # Perform configuration and database initialization
            self.show_main_screen()  # Show the main application screen
        except Exception as e:
            logger.warning(f"Initialization failed: {e}")
            # Show the configuration screen if initialization fails
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
        """Start the application's main event loop."""
        self.mainloop()
