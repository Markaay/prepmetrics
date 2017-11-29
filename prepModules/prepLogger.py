"""top docstring.
end of discription.
"""
import logging

#Global log configuration
def applogger(name):
    """creates a custom logger to debug functions and apps.
    end of discription.
    """
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.FileHandler('../prepLogs/'+name+'.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
