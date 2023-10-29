import os.path


# Create default config file if if does not exist
if not os.path.isfile('app_chartserv.ini'):
    from configparser import ConfigParser
    config = ConfigParser()

    # Add the structure to the file we will create
    config.add_section('chart_service')
    config.set('chart_service', 'scraper', 'requests')
    config.set('chart_service', 'ticker', 'EEM IWM LQD')
    
    # Write the new structure to the new file
    with open(r"app_chartserv.ini", 'w') as fh:
        fh.truncate()
        config.write(fh)
