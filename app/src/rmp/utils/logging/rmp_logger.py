import logging
import yaml
from datetime import datetime
import os
from pathlib import Path


def main():
    e = datetime.now()
    dir_path = os.path.join(os.environ['DATAROOT'], 'logging')
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler("{0}/{1}.log".format(dir_path, e))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


main()
