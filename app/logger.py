


logtime = time.strftime('%Y%m%d')
logging_file = (path + 'deploy_' + logtime + '.log')  # файл, в который пишем лог
formatter = logging.Formatter('[%(asctime)s][%(levelname)-4s] : %(message)s', datefmt='%d/%m/%Y %H:%M:%S')  # формат лога
handlers = \
    [
        logging.handlers.RotatingFileHandler
            (
                logging_file,
                encoding='utf8',
                maxBytes=100000,
                backupCount=1
            ),
        logging.StreamHandler()
    ]
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for handler in handlers:
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)