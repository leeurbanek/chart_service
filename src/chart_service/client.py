import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def get_chart(ctx):
    """"""
    debug = ctx.obj['default']['debug'] == 'True'

    if debug: logger.debug(f"get_chart(ctx={ctx.obj})")

    # check 'chart' folder exists in users 'temp_dir', if not create 'chart' folder
    Path(f"{ctx.obj['default']['temp_dir']}/chart").mkdir(parents=True, exist_ok=True)

    if not debug: print(f"saving to '{ctx.obj['default']['temp_dir']}/chart'\nstarting download")

    [download(ctx, p, s.strip(',')) for p in ctx.obj['chart_service']['period'] for s in ctx.obj['chart_service']['symbol']]

    if not debug: print('cleaning up... ', end='')
    if not debug: print('\b finished')


def download(ctx, period, symbol):
    """"""
    debug = ctx.obj['default']['debug'] == 'True'

    if debug: logger.debug(f"download(ctx={ctx}, period={period}, symbol={symbol})")

    if ctx.obj['chart_service']['scraper'] == 'requests':
        from src.chart_service.scraper import MyRequests
        start = MyRequests(ctx, period, symbol)
    elif ctx.obj['chart_service']['scraper'] == 'selenium':
        from src.chart_service.scraper import MySelenium
        start = MySelenium(ctx, period, symbol)

    try:
        if debug: logger.debug(f"{start}")
        start.webscraper()
    except Exception as e:
        if debug: logger.debug(f"start.webscraper(): {e}")
        pass
