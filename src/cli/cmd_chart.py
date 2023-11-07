import logging

import click

from src import debug
from src.chart_service import client


logger = logging.getLogger(__name__)

@click.command('chart', short_help="Fetch online stockcharts from StockCharts.com", help="""
\b
NAME
    chart -- Get online stock charts from StockChart.com
\b
SYNOPSIS
    chart [Options] [ticker1 ticker2 ticker3 ...]
\b
DESCRIPTION
    The chart utility attempts to fetch online stock charts from
    StockCharts.com.  Charts are saved to the directory specified in
    the config settings.  If no ticker symbols are provided the default
    symbols from the config settings are used.
    Try 'markdata-cli config --help' for help with config settings.
""")

@click.argument('symbol', nargs=-1, default=None, required=False, type=str)

@click.option('--all', 'opt_trans', flag_value='all', help='Fetch daily and weekly charts.')
@click.option('--daily', 'opt_trans', flag_value='daily', help='Fetch only daily charts.')
@click.option('--weekly', 'opt_trans', flag_value='weekly', help='Fetch only weekly charts.')

@click.pass_context
def cli(ctx, opt_trans, symbol):
    """Run chart command"""
    if debug: logger.debug(f"cli(opt_trans={opt_trans}, symbol={symbol})")
    if opt_trans:
        # option flag_value to dictionary of lists
        period_dict = {
            'all': ['Daily', 'Weekly'],
            'daily': ['Daily', ],
            'weekly': ['Weekly', ]
            }
        ctx.obj['chart_service']['period'] = period_dict[opt_trans]

        if symbol:  # use symbols from command line input
            ctx.obj['chart_service']['symbol'] = [
                s.upper() for s in list(symbol)
            ]
        else:  # use symbols from config.ini
            import re
            ctx.obj['chart_service']['symbol'] = [
                s.upper() for s in re.findall(r'[^,;\s]+', ctx.obj['chart_service']['ticker'])
            ]

        client.get_chart(ctx)

    else:  # print default message
        click.echo(f"""Usage: markdata chart [OPTIONS] [SYMBOL]...
Try 'markdata chart --help' for help.""")

# subprocess.run(['open', filename], check=True)
