import os.path


# Create default config file if if does not exist
if not os.path.isfile('cfg_chart.ini'):
    from configparser import ConfigParser
    config_parser = ConfigParser(allow_no_value=True)

    # Add the structure to the file we will create
    config_parser.add_section('chart_service')
    config_parser.set('chart_service', 'scraper', 'requests')
    config_parser.set('chart_service', 'symbol', 'EEM IWM LQD')
    
    # Write the new structure to the new file
    with open(r"cfg_chart.ini", 'w') as fh:
        fh.truncate()
        config_parser.write(fh)
