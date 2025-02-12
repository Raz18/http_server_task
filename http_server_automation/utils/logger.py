import logging
from logging.handlers import RotatingFileHandler

class LoggerConfig:
    @staticmethod
    def get_logger(name: str, log_file: str = "app.log"):
        """
        Configures and returns a logger instance.

        Args:
            name (str): Name of the logger (usually the module or class name).
            log_file (str): Path to the log file.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # File handler with rotation
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger