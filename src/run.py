import logging
import os
from configparser import ConfigParser

import click

from src import config_file


logger = logging.getLogger(__name__)


class MyConfigParser(ConfigParser):
    """Parse section/options from config.ini"""
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class MyMultiCommand(click.MultiCommand):
    """Parse command files in cli directory"""
    def list_commands(self, ctx):
        cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cli'))
        cmd_list = []
        for filename in os.listdir(cmd_folder):
            if filename.startswith("cmd_") and filename.endswith(".py"):
                cmd_list.append(filename[4:-3])
        cmd_list.sort()
        return cmd_list

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"src.cli.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=MyMultiCommand)
@click.option(
    '--debug/--no-debug', default=False, help='Enable/disable debug logging.'
    )
@click.version_option(package_name='chartserv-cli')

@click.pass_context
def main_cli(ctx, debug):
    """ChartServ_CLI: stockmarket CHART SERVice Command Line Interface"""
    conf_obj = MyConfigParser()
    conf_obj.read(config_file)
    ctx.obj = conf_obj.as_dict()
    ctx.obj['debug'] = debug
    if debug: logger.debug(f"main_cli(debug={debug})")
