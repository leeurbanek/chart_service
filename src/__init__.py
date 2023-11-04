import logging, logging.config
import os.path
from configparser import ConfigParser

# from dotenv import load_dotenv


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'config.ini')

# Create default config file if if does not exist
if not os.path.isfile(config_file):
    # config_parser = ConfigParser()
    config_parser = ConfigParser(
        converters={'list': lambda x: [i.strip() for i in x.split(',')]}
        )
    # Add the structure to the file we will create
    config_parser.add_section('default')
    config_parser.set('default', 'debug', 'false')
    config_parser.set('default', 'temp_dir', 'temp')    
    # Write the new structure to the new file
    with open(config_file, 'w') as fh:
        fh.truncate()
        config_parser.write(fh)

# Create getlist() converter, used for reading ticker symbols
# config_parser = ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config_parser = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})

config_parser.read(config_file)

# Gather config files from other apps
cfg_list = []
for filename in os.listdir(base_dir):
    if filename.startswith("cfg_") and filename.endswith(".ini"):
        cfg_list.append(filename)
# and add to config object
for item in cfg_list:
    config_parser.read(item)

config_dict = dict(
    (section, dict(
        (option, config_parser.get(section, option)) 
        for option in config_parser.options(section)
        )
    ) for section in config_parser.sections()
)

logger_conf = os.path.join(base_dir, 'logger.ini')
logging.config.fileConfig(fname=logger_conf)
logging.getLogger('unittest').setLevel(logging.WARNING)

if config_dict['default']['debug'].lower() in [1, 'true', 't', 'yes', 'y'] :
    debug = True
    logger = logging.getLogger(__name__)
    logger.debug(f"config: {config_dict}")


# try:
#     load_dotenv()
#     # alpha_key = os.getenv('ALPHA_KEY')
#     # tiingo_key = os.getenv('TIINGO_KEY')
# except:
#     pass


# __all__ = [
#     "_value",
# ]


# def _value(string):
#     """Convert str 'None' or '' to None type
#     ----------------------------------
#     Parse 'None' or '' string in config.ini to Python None type.\n
#     Parameters
#     ----------
#     `string` : str
#         Config parameter value.\n
#     """
#     return None if string in ['None', ''] else string
