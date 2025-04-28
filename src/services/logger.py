import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name, logfile="./logs/app.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh = RotatingFileHandler(logfile, maxBytes=1048576, backupCount=5, encoding="utf-8")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger

app_logger = setup_logger("mcpserver")