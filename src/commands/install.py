import os
import tempfile
import urllib.request
import logging
import zipfile
import re
from argparse import _SubParsersAction, ArgumentParser

from src.scripts.store import Store
from src.scripts.arch import detect_arch, is_windows

logger = logging.getLogger("pvm.install")

def validate_version_format(version: str) -> bool:
    """Validate that version string matches expected format.
    
    Args:
        version: Version string to validate (e.g., '3.11.0')
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))


def validate_zip_contents(zip_file: zipfile.ZipFile) -> bool:
    """Validate zip file contents for security issues.
    
    Args:
        zip_file: ZipFile object to validate
        
    Returns:
        True if safe, False if suspicious content detected
    """
    for member in zip_file.namelist():
        # Check for absolute paths
        if member.startswith('/'):
            logger.error(f"Suspicious zip entry with absolute path: {member}")
            return False
        
        # Check for path traversal
        if '..' in member:
            logger.error(f"Suspicious zip entry with path traversal: {member}")
            return False
        
        # Check for null bytes
        if '\x00' in member:
            logger.error(f"Suspicious zip entry with null byte: {member}")
            return False
    
    return True







def handle_install(args):
    arch = detect_arch()
    version = args.version
    install_dir = os.path.abspath(args.dir)
    
    # Validate version format
    if not validate_version_format(version):
        logger.error(f"Invalid version format: {version}. Expected format: X.Y.Z (e.g., 3.11.0)")
        return
    
    # Use zip
    installer_name = f"python-{version}-{arch}.zip"
    url = f"https://www.python.org/ftp/python/{version}/{installer_name}"

    if os.path.isdir(install_dir):
        if str(input(f"[WARNING] Directory {install_dir} already exists. Overwrite? (y/n): ")).lower() not in ['y', 'yes']:
            logger.info("Installation cancelled by user.")
            return

    def download_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, (downloaded * 100) / total_size)
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            print(f"\rDownloading: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='', flush=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        logger.debug(f"Downloading installer to temporary directory {tmpdir}")
        installer_path = os.path.join(tmpdir, installer_name)
        logger.info(f"Downloading Python {version} from {url}...")
        try:

            urllib.request.urlretrieve(url, installer_path, reporthook=download_progress)
            logger.info("Download complete.")

        except Exception as e:
            logger.error(f"Failed to download: {e}")
            return
        
        try:
            # Validate and extract zip file
            logger.info(f"Extracting {installer_name} to {install_dir}...")
            with zipfile.ZipFile(installer_path, 'r') as zip_ref:
                # Validate zip contents before extraction
                logger.info("Validating zip contents...")
                if not validate_zip_contents(zip_ref):
                    logger.error("Zip file contains suspicious entries. Installation aborted.")
                    return
                logger.info("Zip contents validated successfully.")
                
                zip_ref.extractall(install_dir)
            
    
            logger.info("Extraction complete.")
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            return
        

        version_data = {
            "version": version,
            "dir": install_dir,
            "using": False
        }   

        Store.set_version(version_data)
        logger.info(f"Python {version} installed successfully at {install_dir}.")
    


def install_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'install',
        help='Install a specific Python version'
    )

    parser.add_argument(
        'version',
        help='Python version to install (e.g., 3.11.0)',
    )



    parser.add_argument(
        '--dir',
        help='Installation directory',
        required=True
    )
    
    parser.set_defaults(func=handle_install)

    