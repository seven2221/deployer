import logging
from logging.handlers import RotatingFileHandler
from deployer.app import app
from deployer.app.config import Config
import os
import time

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logtime = time.strftime('%Y%m%d')
    logging_file = (Config.logpath + 'deploy_' + logtime + '.log')
    file_handler = RotatingFileHandler(logging_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)-4s] : %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('deployer startup')


