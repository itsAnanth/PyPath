import os
import logging
from argparse import _SubParsersAction, ArgumentParser

from src.scripts.store import Store

logger = logging.getLogger("pvm.use")

def handle_use(args):
    
    old_index, old_version = Store.get_version(lambda v: v.get("using") is True)
    old_version['using'] = False

    Store.set_version(old_version)
    
    index, version = Store.get_version(lambda v: v["version"] == args.version)

    if not version:
        logger.error(f"Version {args.version} is not installed. Use 'pvm list --all' to see available versions.")
        return
    
    shimsdir = os.path.join(Store.get_pvm_root(), "shims")

    logger.debug(version)

    
    python_exe = os.path.join(version['dir'], 'python.exe')
    
    # Create python.cmd shim
    python_shim = os.path.join(shimsdir, 'python.cmd')
    with open(python_shim, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'"{python_exe}" %*\n')
    

    
    # Create pip.cmd shim
    pip_shim = os.path.join(shimsdir, 'pip.cmd')
    with open(pip_shim, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'"{python_exe}" -m pip %*\n')
    
    logger.info(f"Using Python {args.version}")

    version['using'] = True
    Store.set_version(version)



    
    


def use_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'use',
        help='Use a specific version of Python which is installed.'
    )

    parser.add_argument(
        'version',
        help='Python version to use',
    )



    parser.set_defaults(func=handle_use)

    