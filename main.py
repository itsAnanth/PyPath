import argparse
from src.scripts.get_versions import get_python_versions

from src.commands.list import list_command
from src.commands.install import install_command

def cli():
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
