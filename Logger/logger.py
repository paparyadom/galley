from logging.handlers import TimedRotatingFileHandler
from logging import Formatter, getLogger, INFO
import pathlib

pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
logfile_name = './logs/galley'
Logger = getLogger('galley')
Logger.setLevel(INFO)
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = TimedRotatingFileHandler(logfile_name, when='midnight', backupCount=15)
fh.setFormatter(formatter)
Logger.addHandler(fh)