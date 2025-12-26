import re
import zipfile
import logging

logger = logging.getLogger("pvm.functions")

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