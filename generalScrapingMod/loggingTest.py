import logging
logger = logging.getLogger(__name__)
def log_setup():
    logging.basicConfig(filename="logs/parkingScript.log",level=logging.INFO,) #INFO change this to the current script path if a path does not exist create the file
    logger.info("Parking Script Started")

log_setup()
