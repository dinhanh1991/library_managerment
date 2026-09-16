import logging

LOGGER = logging.getLogger("library_management")
if not LOGGER.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)

LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False
