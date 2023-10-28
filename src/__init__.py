import logging.config
import os.path
# from dotenv import load_dotenv


# Create default config file if if does not exist
if not os.path.isfile('config.ini'):
    from configparser import ConfigParser
    # config = ConfigParser()
    config_obj = ConfigParser(
        converters={'list': lambda x: [i.strip() for i in x.split(',')]}
        )

    # Add the structure to the file we will create
    config_obj.add_section('default')
    config_obj.set('default', 'debug', 'false')
    config_obj.set('default', 'temp_dir', 'temp')
    
    # Write the new structure to the new file
    with open(r"config.ini", 'w') as fh:
        fh.truncate()
        config_obj.write(fh)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, 'config.ini')

# Create getlist() converter, used in cmd_config.py for ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={'list': lambda x: [i.strip() for i in x.split(',')]})
# config_obj = ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})

logger_conf = os.path.join(base_dir, 'logger.ini')
logging.config.fileConfig(fname=logger_conf)
logging.getLogger('unittest').setLevel(logging.WARNING)


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
