import argparse
import logging
from src.scripts.store import Store
from src.scripts.arch import is_windows
from src.commands.list import list_command
from src.commands.install import install_command

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("pvm")

def cli():

    if not is_windows():
        print("This tool is only support for windows.")
        return
    
    Store.init_store()
    
    parser = argparse.ArgumentParser(
        prog="python-version-manager",
        description="Manage Python versions"
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar=""
    )

    list_command(subparsers)
    install_command(subparsers)


    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)



if __name__ == "__main__":
    cli()
