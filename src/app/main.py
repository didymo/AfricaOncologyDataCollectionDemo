from app.utils.logger import setup_logger
from src.app.gui.app import Application

logger = setup_logger()


def main():
    logger.info("Starting the application...")
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
