"""creates a custom logger for specific apps"""

#Global log configuration
def applogger(name):
    """creates a custom logger to debug functions and apps"""
    import logging
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.FileHandler(name+'.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
