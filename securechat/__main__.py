from enum import Enum, auto, unique
from textwrap import dedent
from typing import Optional

import click

from .__version__ import __version__
from ._const import MODULE_NAME, PRIVATE_KEY, PUBLIC_KEY,HOST,PORT

from .key import generateKeys, loadKeysBase64

COMMAND_EPILOG = dedent(
    """\
    Issue tracker: https://github.com/VillSource/secure-chat/issues
    """
)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj={})



@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, message="%(prog)s %(version)s")
@click.pass_context
def cmd(ctx):
    """
    common securechat help
    """
    pass

@cmd.command(epilog=COMMAND_EPILOG)
def genkey():
    generateKeys()
    print(*loadKeysBase64())

@cmd.command(epilog=COMMAND_EPILOG)
def showkey():
    print(*loadKeysBase64())

@cmd.command(epilog=COMMAND_EPILOG)
@click.option("--host", default="", type=str)
@click.option("--port", default=65432, type=int)
@click.option("--max-client", default=10, type=int)
def runserver(host, port, max_client):
    from .server import startServer
    startServer(host,port, max_client)

@cmd.command(epilog=COMMAND_EPILOG)
@click.option("--host", default="server", type=str)
@click.option("--port", default=65432, type=int)
def connect(host,port):
    from .client import goChat
    goChat(host,port)


if __name__ == "__main__":
    cmd()
