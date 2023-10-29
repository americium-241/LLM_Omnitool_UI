import logging
import os 
from config import LOGGER_LEVEL


local_DIR= os.path.dirname(os.path.realpath(__file__))
# Configure the logging settings
#logger.debug;logger.info;logger.warning;logger.error;logger.critical
def configure_logger():
    logging.basicConfig(
        level=LOGGER_LEVEL,  # Set the logging level to DEBUG
        format='%(asctime)s - %(module)s \n - %(levelname)s - %(message)s \n',  # Define the log format
        handlers=[
        logging.FileHandler(local_DIR+"//Omnitool_UI.log"),
        logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = configure_logger()
