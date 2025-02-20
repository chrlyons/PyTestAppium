import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class LoggerSetup:
    """Utility class for setting up logging with both console and file output"""

    @staticmethod
    def setup_logger(
        logger_name="mobile_testing", log_to_console=True, log_level=logging.INFO
    ):
        """
        Configure a logger with console and file handlers

        Args:
            logger_name: Name of the logger
            log_to_console: Whether to log to console
            log_level: Logging level (default: INFO)

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        if logger.handlers:
            logger.handlers.clear()

        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            logger.addHandler(console_handler)

        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        logs_dir = os.path.join(project_root, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Create timestamped log file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"{logger_name}_{timestamp}.log")

        # Add rotating file handler - max 10MB size, keeping 5 backup files
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10 MB
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        logger.info(f"Logger initialized - output to: {log_file}")

        return logger

    @staticmethod
    def get_logger(name=None):
        """
        Get a pre-configured logger or child logger

        Args:
            name: Optional name for child logger

        Returns:
            Logger instance
        """
        logger_name = "mobile_testing"

        logger = logging.getLogger(logger_name)
        if not logger.handlers:
            logger = LoggerSetup.setup_logger(logger_name)

        if name:
            return logger.getChild(name)

        return logger
