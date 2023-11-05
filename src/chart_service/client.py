import logging
from pathlib import Path

from src import debug

# # Select which version of the webscraper to use
# from src.chart_service.scraper.my_requests import WebScraper
# # from src.chart_service.scraper.my_selenium import WebScraper

# if scraper == 'requests':
#     from src.chart_service.scraper.my_requests import WebScraper
# elif scraper == 'selenium':
#     from src.chart_service.scraper.my_selenium import WebScraper

logger = logging.getLogger(__name__)


def get_chart(ctx):
    """"""
    if debug: logger.debug(f"get_chart(ctx={ctx.obj})")

    # check 'chart' folder exists in users 'temp_dir', if not create 'chart' folder
    Path(f"{ctx.obj['default']['temp_dir']}/chart").mkdir(parents=True, exist_ok=True)

    if not debug: print(f"Saving to '{ctx.obj['default']['temp_dir']}/chart'\nstarting download")

    # [download(p, s.strip(',')) for p in ctx.obj['chart_service']['period'] for s in ctx.obj['chart_service']['ticker']]
    download(ctx=ctx)

    if not debug: print('cleaning up... ', end='')
    if not debug: print('\b finished.')


# def download(period, symbol):
def download(ctx):
    """"""
    scraper = ctx.obj['chart_service']['scraper']
    period = ctx.obj['chart_service']['period']
    symbol = ctx.obj['chart_service']['ticker']

    if debug: logger.debug(f"download(ctx={ctx.obj})")

    if scraper == 'requests':
        from src.chart_service.scraper.my_requests import WebScraper
    elif scraper == 'selenium':
        from src.chart_service.scraper.my_selenium import WebScraper
 
    # [WebScraper(p, s.strip(',')) for p in period for s in symbol]

    start = WebScraper(period=period, symbol=symbol)
    try:
        # [start.webscraper(p, s.strip(',')) for p in period for s in symbol]
        [start.webscraper() for p in period for s in symbol]
    except:
        pass

    # start = WebScraper(debug, period, symbol)
    # try:
    #     start.webscraper()
    # except:
    #     pass

    # [download(p, s.strip(',')) for p in period for s in symbol]
