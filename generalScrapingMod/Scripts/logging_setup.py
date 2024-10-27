import logging
def log_setup(log_file_name):
    logging.basicConfig(filename=f"../logs/{log_file_name}",level=logging.INFO) #INFO change this to the current script path if a path does not exist create the file
    logger = logging.getLogger(__name__)
    return logger


