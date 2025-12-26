import os
import json
import logging

logger = logging.getLogger("pvm.store")

PVM_ROOT = os.path.join(os.environ['LOCALAPPDATA'], '.pvm')
VERSIONS_FILE = os.path.join(PVM_ROOT, 'versions.json')


class Store:

    @staticmethod
    def init_store():
        os.makedirs(PVM_ROOT, exist_ok=True)
        logger.debug(f"Initialized store at {PVM_ROOT}")

        if not os.path.exists(VERSIONS_FILE):
            Store.write_versions([])
            logger.debug(f"Created versions file at {VERSIONS_FILE}")

    @staticmethod
    def get_pvm_root() -> str:
        return PVM_ROOT
    
    @staticmethod
    def get_versions():
        """Read installed versions from JSON file"""
        if not os.path.exists(VERSIONS_FILE):
            return []
        
        with open(VERSIONS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logger.error("Failed to decode versions file, returning empty list")
            return []
    
    @staticmethod
    def write_versions(versions):
        """Write installed versions to JSON file
        
        Args:
            versions: List of dicts with format [{"version": "3.11.0", "dir": "C:\\..."}]
        """
        with open(VERSIONS_FILE, 'w') as f:
            json.dump(versions, f, indent=2)
    
    @staticmethod
    def add_version(version: str, directory: str):
        """Add a new version to the store
        
        Args:
            version: Version of python being added
            directory: install directory
        """
        versions = Store.get_versions()
        versions.append({"version": version, "dir": directory})
        Store.write_versions(versions)
    
    @staticmethod
    def remove_version(version: str):
        """Remove a version from the store
        
        Args:
            version: particular version of python to remove
            
        """
        versions = Store.get_versions()
        versions = [v for v in versions if v["version"] != version]
        Store.write_versions(versions)
    
    @staticmethod
    def get_version_dir(version: str):
        """Get the installation directory for a specific version"""
        versions = Store.get_versions()
        for v in versions:
            if v["version"] == version:
                return v["dir"]
        return None
