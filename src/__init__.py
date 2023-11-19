"""src.__init__.py"""
import logging, logging.config
import os.path
from configparser import ConfigParser


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'config.ini')


# Create getlist() converter, used for reading ticker symbols
# config_parser = ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
config_parser = ConfigParser(
    allow_no_value=True, 
    converters={'list': lambda x: [i.strip() for i in x.split(',')]}
    )

# Create default config file if if does not exist
if not os.path.isfile(config_file):
    # Add the structure to the file we will create
    config_parser.add_section('default')
    config_parser.set('default', 'debug', 'false')
    config_parser.set('default', 'temp_dir', 'temp')    
    # Write the new structure to the new file
    with open(config_file, 'w') as fh:
        fh.truncate()
        config_parser.write(fh)

config_parser.read(config_file)

# Gather config files from other apps
cfg_list = []
for filename in os.listdir(base_dir):
    if filename.startswith("cfg_") and filename.endswith(".ini"):
        cfg_list.append(filename)
# and add to config object
for item in cfg_list:
    config_parser.read(item)

# Put config section/option data into a dictionary
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

# Set debug
debug = False
if config_dict['default']['debug'].lower() in [1, 'true', 't', 'yes', 'y'] :
    config_dict['default']['debug'] = 'True'
    debug = True
else:
    config_dict['default']['debug'] = 'False'

logger = logging.getLogger(__name__)
if debug: logger.debug(f"config_dict = {config_dict}")
