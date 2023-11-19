import logging
import os

import click

from src import config_dict


logger = logging.getLogger(__name__)


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
# @click.option(
#     '--debug/--no-debug', default=False, help='Enable/disable debug logging.'
#     )
@click.version_option(package_name='chartserv-cli')

@click.pass_context
def main_cli(ctx):
    """ChartServ_CLI: stockmarket CHART SERVice Command Line Interface"""
    ctx.obj = config_dict
    if ctx.obj['default']['debug'] == 'True':
        logger.debug(f"main_cli(ctx={ctx.obj})")
