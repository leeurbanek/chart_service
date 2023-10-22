import logging.config
import os
from configparser import ConfigParser

from dotenv import load_dotenv


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'config.ini')

# Create getlist() converter, used in cmd_config.py for ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config_obj = ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})

logger_conf = os.path.join(base_dir, 'logger.ini')
logging.config.fileConfig(fname=logger_conf)
logging.getLogger('unittest').setLevel(logging.WARNING)


try:
    load_dotenv()
    # alpha_key = os.getenv('ALPHA_KEY')
    # tiingo_key = os.getenv('TIINGO_KEY')
except:
    pass


__all__ = [
    "_value",
]


def _value(string):
    """Convert str 'None' or '' to None type
    ----------------------------------
    Parse 'None' or '' string in config.ini to Python None type.\n
    Parameters
    ----------
    `string` : str
        Config parameter value.\n
    """
    return None if string in ['None', ''] else string
