import logging

# Initialize and configure the logger
def setup_logger(log_file="usb_security_manager.log"):
    logger = logging.getLogger("USB_Security_Manager")
    logger.setLevel(logging.INFO)

    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Example utility function for logging actions
def log_action(logger, action_message, level="info"):
    if level.lower() == "info":
        logger.info(action_message)
    elif level.lower() == "warning":
        logger.warning(action_message)
    elif level.lower() == "error":
        logger.error(action_message)
