import logging
from pathlib import Path

from src import debug


logger = logging.getLogger(__name__)


def get_chart(ctx):
    """"""
    scraper = ctx.obj['chart_service']['scraper']

    if debug: logger.debug(f"get_chart(ctx={ctx.obj})")

    # check 'chart' folder exists in users 'temp_dir', if not create 'chart' folder
    Path(f"{ctx.obj['default']['temp_dir']}/chart").mkdir(parents=True, exist_ok=True)

    if not debug: print(f"Saving to '{ctx.obj['default']['temp_dir']}/chart'\nstarting download")

    [download(ctx, p, s.strip(',')) for p in ctx.obj['chart_service']['period'] for s in ctx.obj['chart_service']['symbol']]

    if not debug: print('cleaning up... ', end='')
    if not debug: print('\b finished.')


def download(ctx, period, symbol):
    """"""
    if debug: logger.debug(f"download(ctx={ctx}, period={period}, symbol={symbol})")

    if ctx.obj['chart_service']['scraper'] == 'requests':
        from src.chart_service.scraper.my_requests import WebScraper
    elif ctx.obj['chart_service']['scraper'] == 'selenium':
        from src.chart_service.scraper.my_selenium import WebScraper
 
    start = WebScraper(ctx, period, symbol)

    try:
        start.webscraper()
        if debug: logger.debug(f"{start}")
    except:
        if debug: logger.debug(f"{Exception.mro}")
        pass
