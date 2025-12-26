import argparse
import logging
from src.scripts.store import Store
from src.scripts.arch import is_windows
from src.commands.list import list_command
from src.commands.install import install_command
from src.commands.use import use_command
from src.commands.link import link_command

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("pvm")

def cli():

    if not is_windows():
        logger.info("This tool is only supported for Windows.")
        return
    
    Store.init_store()
    
    parser = argparse.ArgumentParser(
        prog="pvm",
        description="A lightweight Python version manager for Windows. Install, manage, and switch between multiple Python versions with ease. Downloads official embeddable Python distributions, maintains isolated installations, and uses shims for seamless version switching without modifying system settings or registry."
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        metavar=""
    )

    list_command(subparsers)
    install_command(subparsers)
    use_command(subparsers)
    link_command(subparsers)


    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)



if __name__ == "__main__":
    cli()
